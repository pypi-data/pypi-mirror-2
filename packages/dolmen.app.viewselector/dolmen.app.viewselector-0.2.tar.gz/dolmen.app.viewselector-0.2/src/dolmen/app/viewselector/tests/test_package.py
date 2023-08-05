# -*- coding: utf-8 -*-

import unittest
from dolmen.app.viewselector import tests
from zope.testing import doctest
from zope.security.testing import Principal, Participation
from zope.security.management import newInteraction, endInteraction


def login(id, request=None):
    if request is None:
        participation = Participation(Principal(id))
        newInteraction(participation)
    else:
        principal = Principal(id)
        request.setPrincipal(principal)
        newInteraction(request)


def logout():
    endInteraction()


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt',
        globs={'__name__': 'dolmen.app.viewselector',
               'login': login, 'logout': logout},
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    readme.layer = tests.DolmenViewSelectorLayer(tests)
    suite.addTest(readme)
    return suite
