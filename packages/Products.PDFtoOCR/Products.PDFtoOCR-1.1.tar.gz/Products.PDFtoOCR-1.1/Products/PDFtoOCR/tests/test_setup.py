import unittest
import doctest

from Testing import ZopeTestCase as ztc

#from zope.component import getUtility
#from zope.testing import doctestunit
#import zope.component.testing
#
#from Products.CMFCore.utils import getToolByName

from Products.PDFtoOCR.tests.base import pdftoocrTestCase

def test_suite():
    suite = unittest.TestSuite()

    suite.addTest(ztc.FunctionalDocFileSuite(
        'tests/pdftoocr.txt', package='Products.PDFtoOCR',
        test_class=pdftoocrTestCase,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS))


    return suite
