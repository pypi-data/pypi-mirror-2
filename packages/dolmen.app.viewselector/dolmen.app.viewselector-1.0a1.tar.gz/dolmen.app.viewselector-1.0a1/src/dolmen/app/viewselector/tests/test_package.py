# -*- coding: utf-8 -*-

import unittest
import zope.component
from dolmen.app.viewselector import tests
from zope.testing import doctest, module
from zope.security.testing import Principal, Participation
from zope.security.management import newInteraction, endInteraction
from zope.site.folder import rootFolder
from zope.site.site import LocalSiteManager


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


def SiteSetUp(test):
    module.setUp(test, 'dolmen.app.viewselector.tests')
    site = rootFolder()
    site.setSiteManager(LocalSiteManager(site))
    zope.component.hooks.setSite(site)


def tearDown(test):
    zope.component.hooks.resetHooks()
    zope.component.hooks.setSite()
    module.tearDown(test)


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt', setUp=SiteSetUp, tearDown=tearDown,
        globs={'login': login, 'logout': logout},
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    readme.layer = tests.DolmenViewSelectorLayer(tests)
    suite.addTest(readme)
    return suite
