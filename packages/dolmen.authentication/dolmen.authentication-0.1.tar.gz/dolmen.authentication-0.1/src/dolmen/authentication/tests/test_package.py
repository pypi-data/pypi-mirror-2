# -*- coding: utf-8 -*-

import unittest
from dolmen.authentication import tests
from zope.testing import doctest


def interfaceDescription(interface):
    for name, attr in interface.namesAndDescriptions():
        print "%s: %s" % (name, attr.getDoc())


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt',
        globs={'__name__': 'dolmen.authentication',
               'interfaceDescription': interfaceDescription},
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    readme.layer = tests.DolmenAuthentication(tests)
    suite.addTest(readme)
    return suite
