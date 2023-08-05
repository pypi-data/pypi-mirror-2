import unittest
from collective.hook import event

class Test(unittest.TestCase):
    
    def setUp(self):
        self.event = event.HookEvent()

    def testBefore(self):
        #initialization, the event must already be at before=True
        self.assert_(self.event.before)
        self.event.after = True
        self.assert_(not self.event.before)

    def testAfter(self):
        self.assert_(not self.event.after)
        self.event.after = True
        self.assert_(self.event.after)
        #test toggle
        self.event.after = False
        self.event.before = False
        self.assert_(self.event.after)

def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above
    """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    return suite
