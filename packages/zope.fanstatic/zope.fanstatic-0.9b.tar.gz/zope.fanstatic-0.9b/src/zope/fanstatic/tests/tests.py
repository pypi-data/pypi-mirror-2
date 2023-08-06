import unittest
import doctest

from zope.interface import Interface
from zope.component import getGlobalSiteManager
from zope.publisher.interfaces.browser import IBrowserRequest

import fanstatic
from zope.fanstatic.zcml import create_factory
from zope.fanstatic.tests.view import foo
from zope.fanstatic.testing import ZopeFanstaticBrowserLayer
import zope.fanstatic.tests

class TestLayer(ZopeFanstaticBrowserLayer):

    def testSetUp(self):
        super(TestLayer, self).testSetUp()
        # Because it is difficult to dynamically register a
        # entry_point in tests, we do the setup by hand:
        resource_factory = create_factory(foo)
        getGlobalSiteManager().registerAdapter(
            resource_factory, (IBrowserRequest,), Interface, foo.name)

    def setup_middleware(self, app):
        return fanstatic.Injector(app)

layer = TestLayer(zope.fanstatic.tests)

def test_suite():
    readme = doctest.DocFileSuite(
        '../README.txt',
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    readme.layer = layer
    return unittest.TestSuite([readme])
