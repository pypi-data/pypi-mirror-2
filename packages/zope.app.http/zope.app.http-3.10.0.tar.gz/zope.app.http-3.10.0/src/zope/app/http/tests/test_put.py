##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
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
"""Test HTTP PUT verb

$Id: test_put.py 119895 2011-01-25 09:50:21Z icemac $
"""
from unittest import TestCase, TestSuite, makeSuite
from StringIO import StringIO

from zope.interface import implements
from zope.publisher.browser import TestRequest
from zope.filerepresentation.interfaces import IWriteFile
from zope.filerepresentation.interfaces import IWriteDirectory, IReadDirectory, IFileFactory


import zope.app.http.put
from zope.location.interfaces import ILocation
from zope.site.folder import rootFolder
from zope.app.wsgi.testlayer import BrowserLayer

class File(object):

    implements(IWriteFile, ILocation)

    def __init__(self, name, content_type, data):
        self.name = name
        self.content_type = content_type
        self.data = data

    def write(self, data):
        self.data = data

class Container(object):

    implements(IWriteDirectory, IReadDirectory, IFileFactory, ILocation)

    __name__ = None
    __parent__ = None

    def __init__(self, path):
        self.path = path

    def __setitem__(self, name, object):
        object.__name__ = name
        object.__parent__ = self
        setattr(self, name, object)

    def __getitem__(self, name):
        return getattr(self, name)

    def __call__(self, name, content_type, data):
        return File(name, content_type, data)


class TestNullPUT(TestCase):

    layer = BrowserLayer(zope.app.http)

    def test(self):
        self.rootFolder = rootFolder()

        container = Container("put")
        self.rootFolder["put"] = container
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               })
        null = zope.app.http.put.NullResource(container, 'spam.txt')
        put = zope.app.http.put.NullPUT(null, request)
        self.assertEqual(getattr(container, 'spam', None), None)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        file = getattr(container, 'spam.txt')
        self.assertEqual(file.__class__, File)
        self.assertEqual(file.name, 'spam.txt')
        self.assertEqual(file.content_type, 'test/foo')
        self.assertEqual(file.data, content)

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 201)
        self.assertEqual(request.response.getHeader("Location"),
                         "http://127.0.0.1/put/spam.txt")

    def test_bad_content_header(self):
        ## The previous behavour of the PUT method was to fail if the request
        ## object had a key beginning with 'HTTP_CONTENT_' with a status of 501.
        ## This was breaking the new Twisted server, so I am now allowing this
        ## this type of request to be valid.
        self.rootFolder = rootFolder()
        container = Container("/put")
        self.rootFolder["put"] = container
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               'HTTP_CONTENT_FOO': 'Bar',
                               })
        null = zope.app.http.put.NullResource(container, 'spam')
        put = zope.app.http.put.NullPUT(null, request)
        self.assertEqual(getattr(container, 'spam', None), None)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 201)

    def test_put_on_invalid_container_raises_MethodNotAllowed(self):
        import zope.publisher.interfaces.http

        request = TestRequest(StringIO(),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': '0',
                               })
        null = zope.app.http.put.NullResource(rootFolder(), 'spam.txt')
        put = zope.app.http.put.NullPUT(null, request)
        self.assertRaises(zope.publisher.interfaces.http.MethodNotAllowed,
                          put.PUT)


class TestFilePUT(TestCase):
    layer = BrowserLayer(zope.app.http)

    def test(self):
        file = File("thefile", "text/x", "initial content")
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               })
        put = zope.app.http.put.FilePUT(file, request)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        self.assertEqual(file.data, content)

    def test_bad_content_header(self):
        ## The previous behavour of the PUT method was to fail if the request
        ## object had a key beginning with 'HTTP_CONTENT_' with a status of 501.
        ## This was breaking the new Twisted server, so I am now allowing this
        ## this type of request to be valid.
        file = File("thefile", "text/x", "initial content")
        content = "some content\n for testing"
        request = TestRequest(StringIO(content),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': str(len(content)),
                               'HTTP_CONTENT_FOO': 'Bar',
                               })
        put = zope.app.http.put.FilePUT(file, request)
        self.assertEqual(put.PUT(), '')
        request.response.setResult('')
        self.assertEqual(file.data, content)

        # Check HTTP Response
        self.assertEqual(request.response.getStatus(), 200)

    def test_put_on_invalid_file_raises_MethodNotAllowed(self):
        import zope.publisher.interfaces.http

        file = object()
        request = TestRequest(StringIO(),
                              {'CONTENT_TYPE': 'test/foo',
                               'CONTENT_LENGTH': '0',
                               })
        put = zope.app.http.put.FilePUT(file, request)
        self.assertRaises(zope.publisher.interfaces.http.MethodNotAllowed,
                          put.PUT)


def test_suite():
    return TestSuite((
        makeSuite(TestFilePUT),
        makeSuite(TestNullPUT),
        ))
