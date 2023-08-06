##############################################################################
#
# Copyright (c) 2011 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from zope.interface import implements
from zope.component import adapter
from zope.publisher.interfaces import IEndRequestEvent
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL
from zope.traversing.interfaces import ITraversable
from zope.errorview.interfaces import IHandleExceptionEvent

import fanstatic

from zope.fanstatic.interfaces import IZopeFanstaticResource

@adapter(IEndRequestEvent)
def set_base_url(event):
    # At first sight it might be better to subscribe to the
    # IBeforeTraverseEvent for ISite objects and only set a base_url
    # then. However, we might be too early in that case and miss out
    # on essential information for computing URLs. One example of such
    # information is that of the virtualhost namespace traversal.
    needed = fanstatic.get_needed()
    if not needed.has_resources():
        # Do nothing if there're no resources needed at all.
        return
    if needed.base_url is None:
        # Only set the base_url if it has not been set just yet.
        #
        # Note that the given context is set to None, resulting in
        # computing a URL to the Application root (while still
        # adhering to the, for example, virtualhost information). In
        # principle this is not correct, as we should compute the URL
        # for the nearest ISite object, but there is no site nor
        # context anymore in the EndRequestEvent (as the request has
        # been "closed", transactions have been handled, and the site
        # is cleared). Since fanstatic resource "registrations" cannot
        # be overridden on a per ISite basis anyway, this is good
        # enough.
        needed.base_url = absoluteURL(None, event.request)

@adapter(IHandleExceptionEvent)
def clear_needed_resources(event):
    needed = fanstatic.get_needed()
    if isinstance(needed, fanstatic.NeededResources):
        needed.clear()

_sentinel = object()

class ZopeFanstaticResource(object):

    # Hack to get ++resource++foo/bar/baz.jpg *paths* working in Zope
    # Pagetemplates. Note that ++resource+foo/bar/baz.jpg *URLs* will
    # not work with this hack!
    #
    # The ZopeFanstaticResource class also implements an __getitem__()
    # / get() interface, to support rendering URLs to resources from
    # code.

    implements(IZopeFanstaticResource, ITraversable, IAbsoluteURL)

    def __init__(self, request, library, name=''):
        self.request = request
        self.library = library
        self.name = name

    def get(self, name, default=_sentinel):
        # XXX return default if given, or NotFound (or something) when
        # not, in case name is not resolved to an actual resource.
        name = '%s/%s' % (self.name, name)
        return ZopeFanstaticResource(self.request, self.library, name=name)

    def traverse(self, name, furtherPath):
        return self.get(name)

    def __getitem__(self, name):
        resource = self.get(name, None)
        if resource is None:
            raise KeyError(name)
        return resource

    def __str__(self):
        needed = fanstatic.get_needed()
        if needed.base_url is None:
            needed.base_url = absoluteURL(None, self.request)
        return needed.library_url(self.library) + self.name

    __call__ = __str__
