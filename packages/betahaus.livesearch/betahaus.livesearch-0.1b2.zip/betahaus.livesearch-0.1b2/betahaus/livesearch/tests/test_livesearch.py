"""This is an integration "unit" test. It uses PloneTestCase because I'm lazy
"""

import unittest

from Products.CMFCore.utils import getToolByName

from Products.PloneTestCase import PloneTestCase as ptc

import re

import base
ptc.setupPloneSite()

class TestLiveSearch(base.TestCase):
    """Test the Livesearch
    """

    def afterSetUp(self):

        """This method is called before each single test. It can be used to
        set up common state. Setup that is specific to a particular test 
        should be done in that test method.
        """ 
        
        

    def beforeTearDown(self):

        """This method is called after each single test. It can be used for
        cleanup, if you need it. Note that the test framework will roll back
        the Zope transaction at the end of each test, so tests are generally
        independent of one another. However, if you are modifying external
        resources (say a database) or globals (such as registering a new
        adapter in the Component Architecture during a test), you may want to
        tear things down here.
        """
    
        
    def test_oneword(self):
        original = self.portal.livesearch_reply('welcome')
        betahaus_live = self.portal.restrictedTraverse('@@livesearch_reply')
        betahaus_live.request.set('q', 'welcome')
        betahaus_res = betahaus_live()
        self.assertEquals(len([match.start() for match in re.finditer(re.escape('LSRow'), original)]),
                          len([match.start() for match in re.finditer(re.escape('LSRow'), betahaus_res)]))

    def test_twowords(self):
        original = self.portal.livesearch_reply('welcome to')
        betahaus_live = self.portal.restrictedTraverse('@@livesearch_reply')
        betahaus_live.request.set('q', 'welcome to')
        betahaus_res = betahaus_live()
        self.assertEquals(len([match.start() for match in re.finditer(re.escape('LSRow'), original)]),
                          len([match.start() for match in re.finditer(re.escape('LSRow'), betahaus_res)]))
    
    def test_no_res(self):
        original = self.portal.livesearch_reply('blablabla')
        betahaus_live = self.portal.restrictedTraverse('@@livesearch_reply')
        betahaus_live.request.set('q', 'blablabla')
        betahaus_res = betahaus_live()
        self.assertEquals(len([match.start() for match in re.finditer(re.escape('LSRow'), original)]),
                          len([match.start() for match in re.finditer(re.escape('LSRow'), betahaus_res)]))
        
def test_suite():

    """This sets up a test suite that actually runs the tests in the class
    above
    """

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestLiveSearch))
    return suite
