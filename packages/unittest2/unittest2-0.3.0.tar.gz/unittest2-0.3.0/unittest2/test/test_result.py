import sys
from cStringIO import StringIO

import unittest2


class Test_TestResult(unittest2.TestCase):
    # Note: there are not separate tests for TestResult.wasSuccessful(),
    # TestResult.errors, TestResult.failures, TestResult.testsRun or
    # TestResult.shouldStop because these only have meaning in terms of
    # other TestResult methods.
    #
    # Accordingly, tests for the aforenamed attributes are incorporated
    # in with the tests for the defining methods.
    ################################################################

    def test_init(self):
        result = unittest2.TestResult()

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 0)
        self.assertEqual(result.shouldStop, False)

    # "This method can be called to signal that the set of tests being
    # run should be aborted by setting the TestResult's shouldStop
    # attribute to True."
    def test_stop(self):
        result = unittest2.TestResult()

        result.stop()

        self.assertEqual(result.shouldStop, True)

    # "Called when the test case test is about to be run. The default
    # implementation simply increments the instance's testsRun counter."
    def test_startTest(self):
        class Foo(unittest2.TestCase):
            def test_1(self):
                pass

        test = Foo('test_1')

        result = unittest2.TestResult()

        result.startTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        result.stopTest(test)

    # "Called after the test case test has been executed, regardless of
    # the outcome. The default implementation does nothing."
    def test_stopTest(self):
        class Foo(unittest2.TestCase):
            def test_1(self):
                pass

        test = Foo('test_1')

        result = unittest2.TestResult()

        result.startTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        result.stopTest(test)

        # Same tests as above; make sure nothing has changed
        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

    # "Called before and after tests are run. The default implementation does nothing."
    def test_startTestRun_stopTestRun(self):
        result = unittest2.TestResult()
        result.startTestRun()
        result.stopTestRun()

    # "addSuccess(test)"
    # ...
    # "Called when the test case test succeeds"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addSuccess(self):
        class Foo(unittest2.TestCase):
            def test_1(self):
                pass

        test = Foo('test_1')

        result = unittest2.TestResult()

        result.startTest(test)
        result.addSuccess(test)
        result.stopTest(test)

        self.assertTrue(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

    # "addFailure(test, err)"
    # ...
    # "Called when the test case test signals a failure. err is a tuple of
    # the form returned by sys.exc_info(): (type, value, traceback)"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addFailure(self):
        class Foo(unittest2.TestCase):
            def test_1(self):
                pass

        test = Foo('test_1')
        try:
            test.fail("foo")
        except:
            exc_info_tuple = sys.exc_info()

        result = unittest2.TestResult()

        result.startTest(test)
        result.addFailure(test, exc_info_tuple)
        result.stopTest(test)

        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 1)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        test_case, formatted_exc = result.failures[0]
        self.assertTrue(test_case is test)
        self.assertIsInstance(formatted_exc, str)

    # "addError(test, err)"
    # ...
    # "Called when the test case test raises an unexpected exception err
    # is a tuple of the form returned by sys.exc_info():
    # (type, value, traceback)"
    # ...
    # "wasSuccessful() - Returns True if all tests run so far have passed,
    # otherwise returns False"
    # ...
    # "testsRun - The total number of tests run so far."
    # ...
    # "errors - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test which raised an
    # unexpected exception. Contains formatted
    # tracebacks instead of sys.exc_info() results."
    # ...
    # "failures - A list containing 2-tuples of TestCase instances and
    # formatted tracebacks. Each tuple represents a test where a failure was
    # explicitly signalled using the TestCase.fail*() or TestCase.assert*()
    # methods. Contains formatted tracebacks instead
    # of sys.exc_info() results."
    def test_addError(self):
        class Foo(unittest2.TestCase):
            def test_1(self):
                pass

        test = Foo('test_1')
        try:
            raise TypeError()
        except:
            exc_info_tuple = sys.exc_info()

        result = unittest2.TestResult()

        result.startTest(test)
        result.addError(test, exc_info_tuple)
        result.stopTest(test)

        self.assertFalse(result.wasSuccessful())
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(len(result.failures), 0)
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.shouldStop, False)

        test_case, formatted_exc = result.errors[0]
        self.assertTrue(test_case is test)
        self.assertIsInstance(formatted_exc, str)

    def testGetDescriptionWithoutDocstring(self):
        result = unittest2.TextTestResult(None, True, 1)
        self.assertEqual(
                result.getDescription(self),
                'testGetDescriptionWithoutDocstring (' + __name__ +
                '.Test_TestResult)')

    def testGetDescriptionWithOneLineDocstring(self):
        """Tests getDescription() for a method with a docstring."""
        result = unittest2.TextTestResult(None, True, 1)
        self.assertEqual(
                result.getDescription(self),
               ('testGetDescriptionWithOneLineDocstring '
                '(' + __name__ + '.Test_TestResult)\n'
                'Tests getDescription() for a method with a docstring.'))

    def testGetDescriptionWithMultiLineDocstring(self):
        """Tests getDescription() for a method with a longer docstring.
        The second line of the docstring.
        """
        result = unittest2.TextTestResult(None, True, 1)
        self.assertEqual(
                result.getDescription(self),
               ('testGetDescriptionWithMultiLineDocstring '
                '(' + __name__ + '.Test_TestResult)\n'
                'Tests getDescription() for a method with a longer '
                'docstring.'))

    def testStackFrameTrimming(self):
        class Frame(object):
            class tb_frame(object):
                f_globals = {}
        result = unittest2.TestResult()
        self.assertFalse(result._is_relevant_tb_level(Frame))
        
        Frame.tb_frame.f_globals['__unittest'] = True
        self.assertTrue(result._is_relevant_tb_level(Frame))

    def testFailFast(self):
        result = unittest2.TestResult()
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addError(None, None)
        self.assertTrue(result.shouldStop)

        result = unittest2.TestResult()
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addFailure(None, None)
        self.assertTrue(result.shouldStop)

        result = unittest2.TestResult()
        result._exc_info_to_string = lambda *_: ''
        result.failfast = True
        result.addUnexpectedSuccess(None)
        self.assertTrue(result.shouldStop)

    def testFailFastSetByRunner(self):
        runner = unittest2.TextTestRunner(stream=StringIO(), failfast=True)
        def test(result):
            self.assertTrue(result.failfast)
        result = runner.run(test)


if __name__ == '__main__':
    unittest2.main()
