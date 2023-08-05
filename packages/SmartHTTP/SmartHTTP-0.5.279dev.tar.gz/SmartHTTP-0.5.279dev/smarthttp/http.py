# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.http
    HTTP Abstraction
    Last changed on 2010-07-14 20:28:21+11:00 rev. 270:af74439e4595 by Dan Kluev <dan@kluev.name>

..
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


HTTP Abstraction
================

.. _smarthttp.http-HTTPRequest:

:class:`HTTPRequest`
--------------------

This class encapsulates parameters and headers of HTTP request.
    It is interface-compatible with :class:`urllib2.Request`

    Should not be instantiated directly, call :func:`smarthttp.sites.SiteHandler.request`
    or :func:`smarthttp.client.HTTPClient.request` instead.
    

.. autoclass:: HTTPRequest
    :members:
    :undoc-members:

.. _smarthttp.http-HTTPResponse:

:class:`HTTPResponse`
---------------------

Abstract encapsulation of HTTP response.
    Should be interface-compatible with :class:`http.client.HTTPResponse`.

    HTTP implementations subclass it and provide own constructors.

    Inherits from :class:`~smarthttp.asserts.ResponseAssertMixIn` to expose validation asserts.
    

.. autoclass:: HTTPResponse
    :members:
    :undoc-members:

.. _smarthttp.http-HTTPError:

:class:`HTTPError`
------------------

Special subclass of :class:`HTTPResponse` for cases of
    HTTP errors. 
    

.. autoclass:: HTTPError
    :members:
    :undoc-members:

.. _smarthttp.http-LocalFile:

:class:`LocalFile`
------------------

Subclass of :class:`HTTPResponse` which is used to load local files.
    

.. autoclass:: LocalFile
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from .exceptions import SmartHTTPException, DocumentError
from .html import HTMLDocument
from .xml  import XMLDocument
from .asserts import ResponseAssertMixIn
import demjson as json
from .urls import URL
from .lib.containers import SmartDict
from httplib import HTTPMessage
from StringIO import StringIO
import logging
log = logging.getLogger(__name__)

class HTTPRequest(object):
    """This class encapsulates parameters and headers of HTTP request.
    It is interface-compatible with :class:`urllib2.Request`

    Should not be instantiated directly, call :func:`smarthttp.sites.SiteHandler.request`
    or :func:`smarthttp.client.HTTPClient.request` instead.
    """
    _url = None
    data = None
    _referer = None
    method  = "GET"
    cookies = None
    user_agent = None
    def __init__(self, url, data=None, referer=None, method=None, user_agent=None, **kw):
        """
        :param url: Instance of :class:`~smarthttp.urls.URL`
        """
        self._url = url
        self.data = data
        self._referer = referer
        self.method = method
        self.user_agent = user_agent

    def set_cookies(self, cookiejar):
        self.cookies = {}
        cookies = cookiejar._cookies_for_request(self)
        for cookie in cookies:
            self.cookies[cookie.name] = cookie.value
    
    @property
    def url(self):
        return self._url.url

    @property
    def referer(self):
        if self._referer:
            return self._referer.url
        else:
            return None

    def get_full_url(self):
        return self._url.url
    
    def get_host(self):
        return self._url.hostname

    def get_origin_req_host(self):
        return self.get_host()

    def is_unverifiable(self):
        return False

    def __repr__(self):
        return "<HTTPRequest({0.method} {0.url})>".format(self)

class HTTPResponse(ResponseAssertMixIn):
    """Abstract encapsulation of HTTP response.
    Should be interface-compatible with :class:`http.client.HTTPResponse`.

    HTTP implementations subclass it and provide own constructors.

    Inherits from :class:`~smarthttp.asserts.ResponseAssertMixIn` to expose validation asserts.
    """
    error = False
    error_text = None
    data  = None
    header = None
    document = None
    date = None
    code = None
    size = None
    _url = None
    headers = None
    type = None
    maintype = None
    subtype = None
    typeparams = None
    charset = None
    client  = None
    mimemessage = None

    def parse_header(self, header):
        header = header.replace('\r\n', '\n').replace('\r', '\n').split('\n')
        while ('HTTP/' in header[0]) or not header[0]:
            header = header[1:]
        self.header = "\n".join(header)
        self.mimemessage = HTTPMessage(StringIO(self.header))
        self.headers = self.mimemessage.dict
        self.type = self.mimemessage.type
        self.subtype = self.mimemessage.subtype
        self.maintype = self.mimemessage.maintype
        self.typeparams = {}
        for tparam in self.mimemessage.plist:
            if '=' in tparam:
                key, value = tparam.split('=', 1)
                self.typeparams[key.strip().lower()] = value.strip()
        self.charset = self.typeparams.get('charset', None)
    
    def _set_url(self, url):
        if not isinstance(url, URL):
            url = URL(url)
        self._url = url
    
    def _get_url(self):
        return self._url.url
        
        
    url = property(_get_url, _set_url)
                    
    ## urllib2.Response object methods
    def info(self):
        return self.mimemessage

    ## urllib2.Request object methods
    def get_full_url(self):
        return self.url
    
    def get_host(self):
        return self._url.hostname

    def get_origin_req_host(self):
        return self.get_host()

    def is_unverifiable(self):
        return False

    ## Parsing properties
    @property
    def json(self):
        """Parse response body as JSON and cache it.
        
        :rtype: :class:`~smarthttp.lib.containers.SmartDict`
        """
        if not self.document:
            if self.data:
                d = json.decode(self.data)
                if d:
                    self.document = SmartDict(d, _strict_check=True, _propagate=True)
            else:
                raise DocumentError("Response is empty, cannot parse.")
        return self.document
            
    @property
    def xml(self):
        """Parse response body as XML and cache it.
        
        :rtype: :class:`~smarthttp.xml.XMLDocument`
        """
        if not self.document:
            if self.data:
                self.document = XMLDocument(request=self)
            else:
                raise DocumentError("Response is empty, cannot parse.")
        return self.document

    @property
    def html(self):
        """Parse response body as HTML and cache it.
        
        :rtype: :class:`smarthttp.html.HTMLDocument`
        """
        if not self.document:
            if self.data:
                self.document = HTMLDocument(request=self)
            else:
                raise DocumentError("Response is empty, cannot parse.")
        return self.document

    dom = html

    @property
    def html5(self):
        """Parse response body as HTML5 with standard-compliant parser
        and cache it as `self.document`.
        
        :rtype: :class:`smarthttp.html.HTMLDocument`
        """
        if not self.document:
            if self.data:
                self.document = HTMLDocument(request=self, html5=True)
            else:
                raise DocumentError("Response is empty, cannot parse.")
        return self.document

    def autoparse(self):
        """Parse response body according to content-type header.
        
        Content-types and parsers are associated as follows:
        
            * XML  application/xml text/xml
            * HTML text/html application/xhtml+xml
            * CSS  text/css
            * JS   application/javascript text/javascript
            * TEXT text/plain

        :rtype: :class:`~smarthttp.lib.containers.SmartDict` or :class:`~smarthttp.xml.XMLDocument` or :class:`smarthttp.html.HTMLDocument`
        """
        if not self.document:
            if self.data:
                if self.type in ['text/html', 'application/xhtml+xml']:
                    return self.html
                elif self.type in ['application/xml', 'text/xml']:
                    return self.xml
                elif self.type in ['application/json', 'application/javascript', 'text/javascript']:
                    return self.json
                else:
                    raise SmartHTTPException("No known parser for {0.type}".format(self))
            else:
                raise DocumentError("Response is empty, cannot parse.")
        return self.document

    def __repr__(self):
        return "<HTTPResponse('{0.url}', {0.code}, {0.size} bytes)>".format(self)

class LocalFile(HTTPResponse):
    """Subclass of :class:`HTTPResponse` which is used to load local files.
    """
    def __init__(self, filepath=None, data=None):
        """Only first valid data source is used.
        
        :param filepath: Path to file
        :param data: Response body

        .. todo: Should deal with urls properly.
        
        """
        if filepath:
            self.data = open(filepath, 'r').read()
        elif data:
            self.data = data

        self.code = 200
        self.url = filepath or ''

class HTTPError(HTTPResponse):
    """Special subclass of :class:`HTTPResponse` for cases of
    HTTP errors. 
    """
    error = True
    def __repr__(self):
        return "<HTTPError('{0.url}', {0.code}, {0.error_text}>".format(self)    
