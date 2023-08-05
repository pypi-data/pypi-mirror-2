import unittest
import copy
from collective.hook import decorator
from zope import event


class Test(unittest.TestCase):
    
    def setUp(self):
        self.global_ = []
        self.handled = []
        @decorator.hook()
        def fake_method(toto):
            self.global_.append(toto)
        def f(event):
            self.handled.append(copy.copy(event))

        del event.subscribers[:]
        event.subscribers.append(f)

        self.func = fake_method

    def testNotificationHappened(self):
        self.func(3)
        self.assertEqual(len(self.global_), 1)
        self.assertEqual(len(self.handled), 2)
    
    def testBeforeAndAfter(self):
        self.func(5)
        self.assertEqual(self.handled[0].before, True)
        self.assertEqual(self.handled[0].after, False)
        self.assertEqual(self.handled[1].before, False)
        self.assertEqual(self.handled[1].after, True)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
