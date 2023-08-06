# -*- coding: utf-8 -*-
"""
Testing SpreadsheetDocument
"""
# $Id$

import unittest
import os
from fixures import *

import openxmllib

class SpreadsheetTest(unittest.TestCase):
    """Testing querying properties from a document"""

    def setUp(self):
        test_file_path = os.path.join(TEST_FILES_IN, ALL_IN_FILES[1])
        self.doc = openxmllib.openXmlDocument(path=test_file_path)
        return


    def test_indexableText(self):
        """Indexable text with properties
        """
        itext = self.doc.indexableText().split()
        some_words = (u'this', u'is', u'a', u'spreadsheet', u'another', u'sum',
            u'myinfo1', u'myinfo2', u'title', u'subject', u'comments', u'midword')
        for word in some_words:
            self.failUnless(word in itext, "%s was expected in %s" % (word, itext))
        return


    def test_indexableTextNoprop(self):
        """Indexable text without properties
        """
        itext = self.doc.indexableText(include_properties=False).split()
        some_words = (u'this', u'is', u'a', u'spreadsheet', u'another', u'sum')
        for word in some_words:
            self.failUnless(word in itext, "%s was expected in %s" % (word, itext))
        return
# /class SpreadsheetTest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SpreadsheetTest))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
