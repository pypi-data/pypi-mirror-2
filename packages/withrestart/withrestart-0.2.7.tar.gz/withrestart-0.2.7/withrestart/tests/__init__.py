
from __future__ import with_statement

import os
import sys
import unittest
import threading
import timeit

import withrestart
from withrestart import *

#import psyco
#withrestart.callstack.enable_psyco_support()
#psyco.full()


def div(a,b):
    return a/b

class TestRestarts(unittest.TestCase):
    """Testcases for the "withrestart" module."""

    def tearDown(self):
        # Check that no stray frames exist in various CallStacks
        try:
            self.assertEquals(len(withrestart._cur_restarts),0)
            self.assertEquals(len(withrestart._cur_handlers),0)
        finally:
            withrestart._cur_restarts.clear()
            withrestart._cur_handlers.clear()

    def test_basic(self):
        def handle_TypeError(e):
            raise InvokeRestart("use_value",7)
        with Handler(TypeError,handle_TypeError):
            with Restart(use_value):
                self.assertEquals(div(6,3),2)
                self.assertEquals(invoke(div,6,3),2)
                self.assertEquals(invoke(div,6,"2"),7)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)

    def test_multiple(self):
        def handle_TE(e):
            raise InvokeRestart("use_value",7)
        def handle_ZDE(e):
            raise InvokeRestart("raise_error",RuntimeError)
        with handlers((TypeError,handle_TE),(ZeroDivisionError,handle_ZDE)):
            with restarts(use_value,raise_error) as invoke:
                self.assertEquals(div(6,3),2)
                self.assertEquals(invoke(div,6,3),2)
                self.assertEquals(invoke(div,6,"2"),7)
                self.assertRaises(RuntimeError,invoke,div,6,0)

    def test_nested(self):
        with Handler(TypeError,"use_value",7):
            with restarts(use_value) as invoke:
                self.assertEquals(div(6,3),2)
                self.assertEquals(invoke(div,6,3),2)
                self.assertEquals(invoke(div,6,"2"),7)
                with Handler(TypeError,"use_value",9):
                    self.assertEquals(invoke(div,6,"2"),9)
                self.assertEquals(invoke(div,6,"2"),7)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                with handlers((ZeroDivisionError,"raise_error",RuntimeError)):
                    self.assertRaises(MissingRestartError,invoke,div,6,0)
                    with restarts(raise_error,invoke) as invoke:
                        self.assertEquals(div(6,3),2)
                        self.assertEquals(invoke(div,6,3),2)
                        self.assertEquals(invoke(div,6,"2"),7)
                        self.assertRaises(RuntimeError,invoke,div,6,0)
                    self.assertRaises(MissingRestartError,invoke,div,6,0)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                self.assertEquals(invoke(div,6,"2"),7)


    def test_default_handlers(self):
        with restarts(use_value) as invoke:
            self.assertEquals(div(6,3),2)
            self.assertEquals(invoke(div,6,3),2)
            self.assertRaises(TypeError,invoke,div,6,"2")
            self.assertRaises(ZeroDivisionError,invoke,div,6,0)
            invoke.default_handlers = Handler(TypeError,"use_value",7)
            self.assertEquals(invoke(div,6,"2"),7)
            self.assertRaises(ZeroDivisionError,invoke,div,6,0)
            with Handler(TypeError,"use_value",9):
                self.assertEquals(invoke(div,6,"2"),9)
            self.assertEquals(invoke(div,6,"2"),7)
            self.assertRaises(ZeroDivisionError,invoke,div,6,0)
            with handlers((ZeroDivisionError,"raise_error",RuntimeError)):
                self.assertRaises(MissingRestartError,invoke,div,6,0)
                with restarts(raise_error,invoke) as invoke:
                    self.assertEquals(div(6,3),2)
                    self.assertEquals(invoke(div,6,3),2)
                    self.assertEquals(invoke(div,6,"2"),7)
                    self.assertRaises(RuntimeError,invoke,div,6,0)
                self.assertRaises(MissingRestartError,invoke,div,6,0)
            self.assertRaises(ZeroDivisionError,invoke,div,6,0)
            self.assertEquals(invoke(div,6,"2"),7)


    def test_skip(self):
        def calculate(i):
            if i == 7:
                raise ValueError("7 is not allowed")
            return i
        def aggregate(items):
            total = 0
            for i in items:
                with restarts(skip,use_value) as invoke:
                    total += invoke(calculate,i)
            return total
        self.assertEquals(aggregate(range(6)),sum(range(6)))
        self.assertRaises(ValueError,aggregate,range(8))
        with Handler(ValueError,"skip"):
            self.assertEquals(aggregate(range(8)),sum(range(8)) - 7)
        with Handler(ValueError,"use_value",9):
            self.assertEquals(aggregate(range(8)),sum(range(8)) - 7 + 9)


    def test_raise_error(self):
        with Handler(TypeError,"raise_error",ValueError):
            with restarts(use_value,raise_error) as invoke:
                self.assertEquals(invoke(div,6,3),2)
                self.assertRaises(ValueError,invoke,div,6,"2")
            with Handler(ValueError,"raise_error",RuntimeError):
                with restarts(use_value,raise_error) as invoke:
                    self.assertEquals(invoke(div,6,3),2)
                    self.assertRaises(RuntimeError,invoke,div,6,"2")
            with Handler(ValueError,"use_value",None):
                with restarts(use_value,raise_error) as invoke:
                    self.assertEquals(invoke(div,6,3),2)
                    self.assertEquals(invoke(div,6,"2"),None)


    def test_threading(self):
        def calc(a,b):
            with restarts(use_value) as invoke:
                return invoke(div,a,b)
        evt1 = threading.Event()
        evt2 = threading.Event()
        evt3 = threading.Event()
        errors = []
        def thread1():
            try:
                self.assertRaises(TypeError,calc,6,"2")
                with Handler(TypeError,"use_value",4):
                    self.assertEquals(calc(6,"2"),4)
                    evt1.set()
                    evt2.wait()
                    self.assertEquals(calc(6,"2"),4)
                    evt3.set()
                self.assertRaises(TypeError,calc,6,"2")
            except Exception, e:
                evt1.set()
                evt3.set()
                errors.append(e)
        def thread2():
            try:
                self.assertRaises(TypeError,calc,6,"2")
                evt1.wait()
                self.assertRaises(TypeError,calc,6,"2")
                def calc2(a,b):
                    with Restart(raise_error) as invoke:
                        return invoke(calc,a,b)
                self.assertRaises(TypeError,calc2,6,"2")
                with Handler(TypeError,"raise_error",ValueError):
                    self.assertRaises(ValueError,calc2,6,"2")
                    evt2.set()
                    evt3.wait()
                    self.assertRaises(ValueError,calc2,6,"2")
                self.assertRaises(TypeError,calc2,6,"2")
                self.assertRaises(TypeError,calc,6,"2")
            except Exception:
                evt2.set()
                errors.append(sys.exc_info())
        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        for e in errors:
            raise e[0], e[1], e[2]


    def test_inline_definitions(self):
        with handlers() as h:
            @h.add_handler
            def TypeError(e):
                raise InvokeRestart("my_use_value",7)
            with restarts() as invoke:
                @invoke.add_restart
                def my_use_value(v):
                    return v
                self.assertEquals(div(6,3),2)
                self.assertEquals(invoke(div,6,3),2)
                self.assertEquals(invoke(div,6,"2"),7)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                @invoke.add_restart(name="my_raise_error")
                def my_raise_error_restart(e):
                    raise e
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                @h.add_handler(exc_type=ZeroDivisionError)
                def handle_ZDE(e):
                    raise InvokeRestart("my_raise_error",RuntimeError)
                self.assertRaises(RuntimeError,invoke,div,6,0)
                invoke.del_restart("my_raise_error")
                self.assertRaises(MissingRestartError,invoke,div,6,0)
                h.del_handler(handle_ZDE)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                @invoke.add_restart(name="my_raise_error")
                def my_raise_error_restart(e):
                    raise e
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)
                @h.add_handler
                def handle_ZeroDivisionError(e):
                    raise InvokeRestart(my_raise_error_restart,RuntimeError)
                self.assertRaises(RuntimeError,invoke,div,6,0)
                invoke.del_restart(my_raise_error_restart)
                self.assertRaises(MissingRestartError,invoke,div,6,0)
                h.del_handler(handle_ZeroDivisionError)
                self.assertRaises(ZeroDivisionError,invoke,div,6,0)


    def test_retry(self):
        call_count = {}
        def callit(v):
            if v not in call_count:
                call_count[v] = v
            else:
                call_count[v] -= 1
            if call_count[v] > 0:
                raise ValueError("call me again")
            return v
        self.assertRaises(ValueError,callit,2)
        self.assertRaises(ValueError,callit,2)
        self.assertEquals(callit(2),2)
        errors = []
        with handlers() as h:
            @h.add_handler(exc_type=ValueError)
            def OnValueError(e):
                errors.append(e)
                raise InvokeRestart("retry")
            with restarts(retry) as invoke:
                self.assertEquals(invoke(callit,3),3)
        self.assertEquals(len(errors),3)

 
    def test_generators(self):
        def if_not_seven(i):
             if i == 7:
                raise ValueError("can't use 7")
             return i
        def check_items(items):
            for i in items:
                with restarts(skip,use_value) as invoke:
                    yield invoke(if_not_seven,i)
        self.assertEquals(sum(check_items(range(6))),sum(range(6)))
        self.assertRaises(ValueError,sum,check_items(range(8)))
        with Handler(ValueError,"skip"):
            self.assertEquals(sum(check_items(range(8))),sum(range(8))-7)
            with Handler(ValueError,"use_value",2):
                self.assertEquals(sum(check_items(range(8))),sum(range(8))-7+2)
            #  Make sure that the restarts inside the suspended generator
            #  are not visible outside it.
            g = check_items(range(8))
            try:
                self.assertEquals(g.next(),0)
                self.assertEquals(find_restart("skip"),None)
            finally:
                g.close()


    def test_overhead(self):
        """Test overhead in comparison to a standard try-except block.

        For compatability with the "timeit" module, the "test_tryexcept"
        and "test_restart" functions used by this test are importable from
        the separate sub-module "withrestart.tests.overhead".
        """
        #  If psyco is in use, we need to muck around getting simulated
        #  frame objects.  All performance bets are off.
        if "psyco" in sys.modules:
            return
        def dotimeit(name,args):
            testcode = "%s(%s)" % (name,args,)
            setupcode = "from withrestart.tests.overhead import %s" % (name,)
            t = timeit.Timer(testcode,setupcode)
            return min(t.repeat(number=10000))
        def assertOverheadLessThan(scale,args):
            t1 = dotimeit("test_tryexcept",args)
            t2 = dotimeit("test_restart",args)
            print "%.4f / %.4f == %.4f" % (t2,t1,t2/t1)
            self.assertTrue(t1*scale > t2)
        #  Restarts not used
        assertOverheadLessThan(20,"4,4")
        #  Restarts not used
        assertOverheadLessThan(20,"100,100")
        #  Restarts used to return default value
        assertOverheadLessThan(27,"7,0")

    def test_callstack(self):
        stack = CallStack()
        stack.push("hello")
        assert list(stack.items()) == ["hello"]
        def testsingle():
            stack.push("world")
            stack.push("how")
            assert list(stack.items()) == ["how","world","hello"]
            stack.pop()
            assert list(stack.items()) == ["world","hello"]
        testsingle()
        assert list(stack.items()) == ["hello"]
        def testnested():
            stack.push("world")
            stack.push("how")
            assert list(stack.items()) == ["how","world","hello"]
            def subtest():
                stack.push("are")
                stack.push("you")
                assert list(stack.items())==["you","are","how","world","hello"]
            subtest()
            assert list(stack.items()) == ["how","world","hello"]
            stack.pop()
            assert list(stack.items()) == ["world","hello"]
        testnested()
        assert list(stack.items()) == ["hello"]
        def testgenerator():
            stack.push("world")
            stack.push("how")
            assert list(stack.items()) == ["how","world","hello"]
            def gen():
                stack.push("are",1)
                stack.push("you")
                assert list(stack.items())==["you","are","how","world","hello"]
                yield None
                assert list(stack.items())==["you","are","how","world","hello"]
                stack.pop()
                yield None
                assert list(stack.items())==["are","how","world","hello"]
            g = gen()
            assert list(stack.items()) == ["how","world","hello"]
            g.next()
            assert list(stack.items()) == ["are","how","world","hello"]
            g.next()
            assert list(stack.items()) == ["are","how","world","hello"]
            try:
                g.next()
            except StopIteration:
                pass
            stack.pop()
            assert list(stack.items()) == ["how","world","hello"]
        testgenerator()
        assert list(stack.items()) == ["hello"]
       


    def test_README(self):
        """Ensure that the README is in sync with the docstring.

        This test should always pass; if the README is out of sync it just
        updates it with the contents of withrestart.__doc__.
        """
        dirname = os.path.dirname
        readme = os.path.join(dirname(dirname(dirname(__file__))),"README.txt")
        if not os.path.isfile(readme):
            f = open(readme,"wb")
            f.write(withrestart.__doc__)
            f.close()
        else:
            f = open(readme,"rb")
            if f.read() != withrestart.__doc__:
                f.close()
                f = open(readme,"wb")
                f.write(withrestart.__doc__)
                f.close()

