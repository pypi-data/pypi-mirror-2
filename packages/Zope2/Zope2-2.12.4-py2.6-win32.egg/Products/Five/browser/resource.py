##############################################################################
#
# Copyright (c) 2004, 2005 Zope Foundation and Contributors.
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
"""Provide basic resource functionality

$Id: resource.py 110405 2010-04-01 16:13:15Z tseaver $
"""
import os
import urllib

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.publisher.browser import fileresource, directoryresource
from zope.app.publisher.fileresource import File, Image
from zope.app.publisher.pagetemplateresource import PageTemplate

from Products.Five.browser import BrowserView


_marker = object()

class Resource(object):
    """A mixin that changes the URL-rendering of resources (__call__).

    In Zope 3, resource URLs are of the form
    nearest_site/@@/resource_name.  Since Zope 2 didn't have support
    for sites from the beginning of the Five integration, resource
    URLs in Zope 2 are of the form context/++resource++resource_name.

    TODO It would be good if that could be changed in the long term,
    thus making this mixin (and probably the other classes in this
    module) obsolete.
    """
    def __call__(self):
        name = self.__name__
        container = self.__parent__

        url = urllib.unquote(absoluteURL(container, self.request))
        if not isinstance(container, DirectoryResource):
            name = '++resource++%s' % name
        return "%s/%s" % (url, name)

class PageTemplateResource(Resource, BrowserView):
    implements(IBrowserPublisher)

    def browserDefault(self, request):
        return self.render, ()

    def publishTraverse(self, request, name):
        raise NotFound(self, name, request)

    def render(self):
        """Rendered content"""
        # ZPublisher might have called setBody with an incorrect URL
        # we definitely don't want that if we are plain html
        self.request.response.setBase(None)
        pt = self.context
        return pt(self.request)

class FileResource(Resource, fileresource.FileResource):
    pass

class ResourceFactory:

    factory = None
    resource = None

    def __init__(self, name, path, resource_factory=None):
        self.__name = name
        self.__rsrc = self.factory(path, name)
        if resource_factory is not None:
            self.resource = resource_factory

    def __call__(self, request):
        resource = self.resource(self.__rsrc, request)
        return resource

def _PageTemplate(self, path, name):
    # PageTemplate doesn't take a name parameter,
    # which makes it different from FileResource.
    # This is probably an error.
    template = PageTemplate(path)
    template.__name__ = name
    return template

class PageTemplateResourceFactory(ResourceFactory):
    """A factory for Page Template resources"""

    factory = _PageTemplate
    resource = PageTemplateResource

class FileResourceFactory(ResourceFactory):
    """A factory for File resources"""

    factory = File
    resource = FileResource

class ImageResourceFactory(ResourceFactory):
    """A factory for Image resources"""

    factory = Image
    resource = FileResource


# we only need this class a context for DirectoryResource
class Directory:

    def __init__(self, path, name):
        self.path = path
        self.__name__ = name

class DirectoryResource(Resource, directoryresource.DirectoryResource):

    resource_factories = {
        'gif':  ImageResourceFactory,
        'png':  ImageResourceFactory,
        'jpg':  ImageResourceFactory,
        'pt':   PageTemplateResourceFactory,
        'zpt':  PageTemplateResourceFactory,
        'html': PageTemplateResourceFactory,
        }

    default_factory = FileResourceFactory

    def getId(self):
        name = self.__name__
        if not name.startswith('++resource++'):
            name = '++resource++%s' % self.__name__
        return name

    def get(self, name, default=_marker):
        path = self.context.path
        filename = os.path.join(path, name)
        isfile = os.path.isfile(filename)
        isdir = os.path.isdir(filename)

        if not (isfile or isdir):
            if default is _marker:
                raise KeyError(name)
            return default

        if isfile:
            ext = name.split('.')[-1]
            factory = self.resource_factories.get(ext, self.default_factory)
        else:
            factory = DirectoryResourceFactory

        resource = factory(name, filename)(self.request)
        resource.__name__ = name
        resource.__parent__ = self
        
        # We need to propagate security so that restrictedTraverse() will
        # work
        resource.__roles__ = self.__roles__
        
        return resource

class DirectoryResourceFactory(ResourceFactory):

    factory = Directory
    resource = DirectoryResource
