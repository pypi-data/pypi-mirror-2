import unittest, doctest

def test_suite():
    globs = {}
    optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocFileSuite(
        'googlevisualization.txt', globs=globs, optionflags=optionflags))
    return suite
