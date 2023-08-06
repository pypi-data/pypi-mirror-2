"""

  withrestart:  structured error recovery using named restart functions

This is a Pythonisation (Lispers might rightly say "bastardisation") of the
restart-based condition system of Common Lisp.  It's designed to make error
recovery simpler and easier by removing the assumption that unhandled errors
must be fatal.

A "restart" represents a named strategy for resuming execution of a function
after the occurrence of an error.  At any point during its execution a
function can push a Restart object onto its call stack.  If an exception
occurs within the scope of that Restart, code higher-up in the call chain can
invoke it to recover from the error and let the function continue execution.
By providing several restarts, functions can offer several different strategies
for recovering from errors.

A "handler" represents a higher-level strategy for dealing with the occurrence
of an error.  It is conceptually similar to an "except" clause, in that one
establishes a suite of Handler objects to be invoked if an error occurs during
the execution of some code.  There is, however, a crucial difference: handlers
are executed without unwinding the call stack.  They thus have the opportunity
to take corrective action and then resume execution of whatever function
raised the error.

For example, consider a function that reads the contents of all files from a 
directory into a dict in memory::

   def readall(dirname):
       data = {}
       for filename in os.listdir(dirname):
           filepath = os.path.join(dirname,filename)
           data[filename] = open(filepath).read()
       return data

If one of the files goes missing after the call to os.listdir() then the
subsequent open() will raise an IOError.  While we could catch and handle the
error inside this function, what would be the appropriate action?  Should
files that go missing be silently ignored?  Should they be re-created with
some default contents?  Should a special sentinel value be placed in the
data dictionary?  What value?  The readall() function does not have enough
information to decide on an appropriate recovery strategy.

Instead, readall() can provide the *infrastructure* for doing error recovery
and leave the final decision up to the calling code.  The following definition
uses three pre-defined restarts to let the calling code (a) skip the missing
file completely, (2) retry the call to open() after taking some corrective
action, or (3) use some other value in place of the missing file::

   def readall(dirname):
       data = {}
       for filename in os.listdir(dirname):
           filepath = os.path.join(dirname,filename)
           with restarts(skip,retry,use_value) as invoke:
               data[filename] = invoke(open,filepath).read()
       return data

Of note here is the use of the "with" statement to establish a new context
in the scope of restarts, and use of the "invoke" wrapper when calling a
function that might fail.  The latter allows restarts to inject an alternate
return value for the failed function.

Here's how the calling code would look if it wanted to silently skip the
missing file::

   def concatenate(dirname):
       with Handler(IOError,"skip"):
           data = readall(dirname)
       return "".join(data.itervalues())

This pushes a Handler instance into the execution context, which will detect
IOError instances and respond by invoking the "skip" restart point.  If this
handler is invoked in response to an IOError, execution of the readall()
function will continue immediately following the "with restarts(...)" block.

Note that there is no way to achieve this skip-and-continue behaviour using an
ordinary try-except block; by the time the IOError has propagated up to the
concatenate() function for processing, all context from the execution of 
readall() will have been unwound and cannot be resumed.

Calling code that wanted to re-create the missing file would simply push a
different error handler::

   def concatenate(dirname):
       def handle_IOError(e):
           open(e.filename,"w").write("MISSING")
           raise InvokeRestart("retry")
       with Handler(IOError,handle_IOError):
           data = readall(dirname)
       return "".join(data.itervalues())

By raising InvokeRestart, this handler transfers control back to the restart
that was  established by the readall() function.  This particular restart
will re-execute the failing function call and let readall() continue with its
operation.

Calling code that wanted to use a special sentinel value would use a handler
to pass the required value to the "use_value" restart::

   def concatenate(dirname):
       class MissingFile:
           def read():
               return "MISSING"
       def handle_IOError(e):
           raise InvokeRestart("use_value",MissingFile())
       with Handler(IOError,handle_IOError):
           data = readall(dirname)
       return "".join(data.itervalues())


By separating the low-level details of recovering from an error from the
high-level strategy of what action to take, it's possible to create quite
powerful recovery mechanisms.

While this module provides a handful of pre-built restarts, functions will
usually want to create their own.  This can be done by passing a callback
into the Restart object constructor::

   def readall(dirname):
       data = {}
       for filename in os.listdir(dirname):
           filepath = os.path.join(dirname,filename)
           def log_error():
               print "an error occurred"
           with Restart(log_error):
               data[filename] = open(filepath).read()
       return data


Or by using a decorator to define restarts inline::

   def readall(dirname):
       data = {}
       for filename in os.listdir(dirname):
           filepath = os.path.join(dirname,filename)
           with restarts() as invoke:
               @invoke.add_restart
               def log_error():
                   print "an error occurred"
               data[filename] = open(filepath).read()
       return data

Handlers can also be defined inline using a similar syntax::

   def concatenate(dirname):
       with handlers() as h:
           @h.add_handler
           def IOError(e):
               open(e.filename,"w").write("MISSING")
               raise InvokeRestart("retry")
           data = readall(dirname)
       return "".join(data.itervalues())


Now finally, a disclaimer.  I've never written any Common Lisp.  I've only read
about the Common Lisp condition system and how awesome it is.  I'm sure there
are many things that it can do that this module simply cannot.  For example:

  * Since this is built on top of a standard exception-throwing system, the
    handlers can only be executed after the stack has been unwound to the
    most recent restart context; in Common Lisp they're executed without
    unwinding the stack at all.
  * Since this is built on top of a standard exception-throwing system, it's
    probably too heavyweight to use for generic condition signalling system.

Nevertheless, there's no shame in pinching a good idea when you see one...

"""

__ver_major__ = 0
__ver_minor__ = 2
__ver_patch__ = 7
__ver_sub__ = ""
__version__ = "%d.%d.%d%s" % (__ver_major__,__ver_minor__,
                              __ver_patch__,__ver_sub__)


import sys

from withrestart.callstack import CallStack
_cur_restarts = CallStack()  # per-frame active restarts
_cur_handlers = CallStack()  # per-frame active handlers


class RestartError(Exception):
    """Base class for all user-visible exceptions raised by this module."""
    pass


class ControlFlowException(Exception):
    """Base class for all control-flow exceptions used by this module."""
    pass


class MissingRestartError(RestartError):
    """Exception raised when invoking a non-existent restart."""
    def __init__(self,name):
        self.name = name
    def __str__(self):
        return "No restart named '%s' has been defined" % (self.name,)


class InvokeRestart(ControlFlowException):
    """Exception raised by handlers to invoke a selected restart.

    This is used as a flow-control mechanism and should never be seen by
    code outside this module.  It's purposely not a sublcass of RestartError;
    you really shouldn't be catching it except under special circumstances.
    """
    def __init__(self,restart,*args,**kwds):
        if not isinstance(restart,Restart):
            name = restart; restart = find_restart(name)
            if restart is None:
                raise MissingRestartError(name)
        self.restart = restart
        self.args = args
        self.kwds = kwds

    def invoke(self):
        """Convenience methods for invoking the selected restart."""
        return self.restart.invoke(*self.args,**self.kwds)

    def __str__(self):
        return "<InvokeRestart '%s' with %s, %s>" % (self.restart.name,self.args,self.kwds)


class ExitRestart(ControlFlowException):
    """Exception raised by restarts to immediately exit their context.

    Restarts can raise ExitRestart to immediately transfer control to the
    end of their execution context.  It's primarily used by the pre-defined
    "skip" restart but others are welcome to use it for similar purposes.

    This is used as a flow-control mechanism and should never be seen by
    code outside this module.  It's purposely not a sublcass of RestartError;
    you really shouldn't be catching it except under special circumstances.
    """
    def __init__(self,restart=None):
        self.restart = restart


class RetryLastCall(ControlFlowException):
    """Exception raised by restarts to re-execute the last function call.

    Restarts can raise RetryLastCall to immediately re-execute the last
    function invoked within a restart context.  It's primarily used by
    the pre-defined "retry" restart but others are welcome to use it for
    similar purposes.

    This is used as a flow-control mechanism and should never be seen by
    code outside this module.  It's purposely not a sublcass of RestartError;
    you really shouldn't be catching it except under special circumstances.
    """
    pass


class RaiseNewError(ControlFlowException):
    """Exception raised by restarts to re-raise a different error.

    Restarts can raise RaiseNewErorr to re-start the error handling machinery
    using a new exception.  This is different to simply raising an exception
    inside the restart function - RaiseNewError causes the new exception to
    be pushed back through the error-handling machinery and potentially handled
    by the same restart context.

    This is used as a flow-control mechanism and should never be seen by
    code outside this module.  It's purposely not a sublcass of RestartError;
    you really shouldn't be catching it except under special circumstances.
    """

    def __init__(self,error):
        self.error = error



class Restart(object):
    """Restart marker object.

    Instances of Restart represent named strategies for resuming execution
    after the occurrence of an error.  Collections of Restart objects are
    pushed onto the execution context where code can cleanly restart after
    the occurrence of an error, but requires information from outside the
    function in order to do so.

    When an individual Restat object is used as a context manager, it will
    automatically wrap itself in a RestartSuite object.
    """

    def __init__(self,func,name=None):
        """Restart object initializer.

        A Restart must be initialized with a callback function to execute
        when the restart is invoked.  If the optional argument 'name' is
        given this becomes the name of the Restart; otherwise its name is
        taken from the callback function.
        """
        self.func = func
        if name is None:
            self.name = func.func_name
        else:
            self.name = name

    def invoke(self,*args,**kwds):
        """Invoke this restart with the given arguments.

        This wrapper method also maintains some internal state for use by
        the restart-handling machinery.
        """
        try:
            return self.func(*args,**kwds)
        except ExitRestart, e:
            e.restart = self
            raise

    def __enter__(self):
        suite =  RestartSuite(self)
        _cur_restarts.push(suite,1)
        return suite

    def __exit__(self,exc_type,exc_value,traceback):
        _cur_restarts.items().next().__exit__(exc_type,exc_value,traceback)


class RestartSuite(object):
    """Class holding a suite of restarts belonging to a common context.

    The RestartSuite class is used to bundle individual Restart objects
    into a set that is pushed/popped together.  It's also possible to
    add and remove individual restarts from a suite dynamically, allowing
    them to be defined inline using decorator syntax.

    If the attribute "default_handlers" is set to a Handler or HandlerSuite
    instance, that instance will be invoked if no other handler has been 
    established for the current exception type.
    """

    def __init__(self,*restarts):
        self.restarts = []
        self.default_handlers = None
        for r in restarts:
            if isinstance(r,RestartSuite):
                for r2 in r.restarts:
                    self.restarts.append(r2)
            elif isinstance(r,Restart):
                self.restarts.append(r)
            else:
                self.restarts.append(Restart(r))

    def add_restart(self,func=None,name=None):
        """Add the given function as a restart to this suite.

        If the 'name' keyword argument is given, that will be used instead
        of the name of the function.  The following are all equivalent:

            def my_restart():
                pass
            r.add_restart(Restart(my_restart,"skipit"))

            @r.add_restart(name="skipit")
            def my_restart():
                pass

            @r.add_restart
            def skipit():
                pass

        """
        def do_add_restart(func):
            if isinstance(func,Restart):
                r = func
            else:
                r = Restart(func,name)
            self.restarts.append(r)
            return func
        if func is None:
            return do_add_restart
        else:
            return do_add_restart(func)

    def del_restart(self,restart):
        """Remove the given restart from this suite.

        The restart can be specified as a Restart instance, function or name.
        """
        to_del = []
        for r in self.restarts:
            if r is restart or r.func is restart or r.name == restart:
                to_del.append(r)
        for r in to_del:
            self.restarts.remove(r)

    def __call__(self,func,*args,**kwds):
        """Invoke the given function in the context of this restart suite.

        If a restart is invoked in response to an error, its return value
        is used in place of the function call.
        """
        exc_type, exc_value, traceback = None, None, None
        try:
            return func(*args,**kwds)
        except InvokeRestart, e:
            if e.restart in self.restarts:
                try:
                    return e.invoke()
                except RetryLastCall:
                    return self(func,*args,**kwds)
                except RaiseNewError, newerr:
                    exc_info = self._normalise_error(newerr.error)
                    exc_type, exc_value = exc_info[:2]
                    if exc_info[2] is not None:
                        traceback = exc_info[2]
            else:
                raise
        except Exception:
            exc_type, exc_value, traceback = sys.exc_info()
        while exc_value is not None:
            try:
                self._invoke_handlers(exc_value)
            except InvokeRestart, e:
                if e.restart in self.restarts:
                    try:
                        return e.invoke()
                    except RetryLastCall:
                        return self(func,*args,**kwds)
                    except RaiseNewError, newerr:
                        exc_info = self._normalise_error(newerr.error)
                        exc_type, exc_value = exc_info[:2]
                        if exc_info[2] is not None:
                            traceback = exc_info[2]
                else:
                    raise
            else:
                raise exc_type, exc_value, traceback

    def _normalise_error(self,error):
        exc_type, exc_value, traceback = None, None, None
        if isinstance(error,BaseException):
            exc_type = type(error)
            exc_value = error
        elif isinstance(error,type):
            exc_type = error
            exc_value = error()
        else:
            values = tuple(error)
            if len(values) == 1:
                exc_type = values[0]
                exc_info = exc_type()
            elif len(values) == 2:
                exc_type, exc_info = values
            elif len(values) == 3:
                exc_type, exc_value, traceback = values
            else:
                raise ValueError("too many items in exception tuple")
        return exc_type, exc_value, traceback

    def __enter__(self):
        _cur_restarts.push(self,1)
        return self

    def __exit__(self,exc_type,exc_value,traceback,internal=False):
        try:
            if exc_type is not None:
                if exc_type is InvokeRestart:
                    for r in self.restarts:
                        if exc_value.restart is r:
                            return self._invoke_restart(exc_value)
                    else:
                        return False
                elif exc_type is ExitRestart:
                    for r in self.restarts:
                        if exc_value.restart is r:
                            return True
                    else:
                        return False
                else:
                    try:
                        self._invoke_handlers(exc_value)
                    except InvokeRestart, e:
                        for r in self.restarts:
                            if e.restart is r:
                                return self._invoke_restart(e)
                        else:
                            raise
                    else:
                        return False
        finally:
            if not internal:
                _cur_restarts.pop()

    def _invoke_restart(self,r):
        try:
            r.invoke()
        except ExitRestart, e:
            if e.restart not in self.restarts:
                raise
        except RetryLastCall:
            return False
        except RaiseNewError, e:
             exc_type, exc_value, traceback = self._normalise_error(e.error)
             return self.__exit__(exc_type,exc_value,traceback,internal=True)
        return True

    def _invoke_handlers(self,e):
        handlers = find_handlers(e)
        if handlers:
            for handler in handlers:
                handler.handle_error(e)
        else:
            if self.default_handlers is not None:
                if isinstance(e,self.default_handlers.exc_type):
                    self.default_handlers.handle_error(e)

#  Convenience name for accessing RestartSuite class.
restarts = RestartSuite


def find_restart(name):
    """Find a defined restart with the given name.

    If no such restart is found then None is returned.
    """
    for suite in _cur_restarts.items():
        for restart in suite.restarts:
            if restart.name == name or restart.func == name:
                return restart
    return None



def invoke(func,*args,**kwds):
    """Invoke the given function, or return a value from a restart.

    This function can be used to invoke a function or callable object within
    the current restart context.  If the function runs to completion its
    result is returned.  If an error occurrs, the handlers are executed and
    the result from any invoked restart becomes the return value of the
    function call.
    """
    try:
        return func(*args,**kwds)
    except Exception, err:
        try:
            for handler in find_handlers(err):
                handler.handle_error(err)
        except InvokeRestart, e:
            try:
                return e.invoke()
            except RetryLastCall:
                return invoke(func,*args,**kwds)
        else:
            raise


class Handler(object):
    """Restart handler object.

    Instances of Handler represent high-level control strategies for dealing
    with errors that have occurred.  They can be thought of as an "except"
    clause the executes at the site of the error instead of unwinding the
    stack.  Handlers push themselves onto the execution context when entered
    and pop themselves when exited.  They will not swallow errors, but
    can cause errors to be swallowed at a lower level of the callstack by
    explicitly invoking a restart.
    """

    def __init__(self,exc_type,func,*args,**kwds):
        """Handler object initializer.

        Handlers must be initialized with an exception type (or tuple of
        types) and a function to be executed when such errors occur.  If
        the given function is a string, it names a restart that will be
        invoked immediately on error.

        Any additional args or kwargs will be passed into the handler
        function when it is executed.
        """
        self.exc_type = exc_type
        self.func = func
        self.args = args
        self.kwds = kwds

    def handle_error(self,e):
        """Invoke this handler on the given error.

        This is a simple wrapper method to implement the shortcut syntax of
        passing the name of a restart directly into the handler.
        """
        if isinstance(self.func,basestring):
            raise InvokeRestart(self.func,*self.args,**self.kwds)
        else:
            self.func(e,*self.args,**self.kwds)

    def __enter__(self):
        _cur_handlers.push(self,1)
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        _cur_handlers.pop()


class HandlerSuite(object):
    """Class to easily combine multiple handlers into a single context.

    HandleSuite objects represent a set of Handlers that are pushed/popped
    as a group.  The suite can also have handlers dynamically added or removed,
    allowing then to be defined in-line using decorator syntax.
    """

    def __init__(self,*handlers):
        self.handlers = []
        self.exc_type = ()
        for h in handlers:
            if isinstance(h,(Handler,HandlerSuite,)):
                self._add_handler(h)
            else:
                self._add_handler(Handler(*h))

    def handle_error(self,e):
        for handler in self.handlers:
            if isinstance(e,handler.exc_type):
                handler.handle_error(e)

    def __enter__(self):
        _cur_handlers.push(self,1)
        return self

    def __exit__(self,exc_type,exc_info,traceback):
        _cur_handlers.pop()

    def add_handler(self,func=None,exc_type=None):
        """Add the given function as a handler to this suite.

        If the given function is already a Handler or HandlerSuite object,
        it is used directory.  Otherwise, if the exc_type keyword argument
        is given, a Handler is created for that exception type.  Finally,
        if exc_type if not specified then is is looked up using the name of
        the given function.  Thus the following are all equivalent:

            def handle_IOError(e):
                pass
            h.add_handler(Handler(IOError,handle_IOError))

            @h.add_handler(exc_type=IOError):
            def handle_IOError(e):
                pass

            @h.add_handler
            def IOError(e):
                pass

        """
        def do_add_handler(func):
            if isinstance(func,(Handler,HandlerSuite,)):
                h = func
            else:
                if exc_type is not None:
                    h = Handler(exc_type,func)
                else:
                    exc_name = func.func_name
                    try:
                        exc = _load_name_in_scope(func,exc_name)
                    except NameError:
                        if exc_name.startswith("handle_"):
                            exc_name = exc_name[7:]
                            exc = _load_name_in_scope(func,exc_name)
                        else:
                            raise
                    h = Handler(exc,func)
            self._add_handler(h)
            return func
        if func is None:
            return do_add_handler
        else:
            return do_add_handler(func)

    def _add_handler(self,handler):
        """Internal logic for adding a handler to the suite.

        This appends the handler to self.handlers, and adjusts self.exc_type
        to reflect the newly-handled exception types.
        """
        self.handlers.append(handler)
        if isinstance(handler.exc_type,tuple):
            self.exc_type = self.exc_type + handler.exc_type
        else:
            self.exc_type = self.exc_type + (handler.exc_type,)

    def del_handler(self,handler):
        """Remove any handlers matching the given value from the suite.

        The 'handler' argument can be a Handler instance, function or
        exception type.
        """
        to_del = []
        for h in self.handlers:
            if h is handler or h.func is handler or h.exc_type is handler:
                to_del.append(h)
        for h in to_del:
            self.handlers.remove(h)

#  Convenience name for accessing HandlerSuite class.
handlers = HandlerSuite


def find_handlers(err):
    """Find the currently-established handlers for the given error.

    This function returns a list of all handlers currently established for
    the given error, in the order in which they should be invoked.
    """
    handlers = []
    for handler in _cur_handlers.items():
        if isinstance(err,handler.exc_type):
            handlers.append(handler)
    return handlers


def skip():
    """Pre-defined restart that skips to the end of the restart context."""
    raise ExitRestart

def retry():
    """Pre-defined restart that retries the most-recently-invoked function."""
    raise RetryLastCall

def raise_error(error):
    """Pre-defined restart that raises the given error."""
    raise RaiseNewError(error)

def use_value(value):
    """Pre-defined restart that returns the given value."""
    return value


def _load_name_in_scope(func,name):
    """Get the value of variable 'name' as seen in scope of given function.

    If no such variable is found in the function's scope, NameError is raised.
    """
    try:
        try:
            idx = func.func_code.co_cellvars.index(name)
        except ValueError:
            try:
                idx = func.func_code.co_freevars.index(name)
                idx -= len(func.func_code.co_cellvars)
            except ValueError:
                raise NameError(name)
        return func.func_closure[idx].cell_contents
    except NameError:
        try:
           try:
                return func.func_globals[name]
           except KeyError:
                return __builtins__[name]
        except KeyError:
             raise NameError(name)

