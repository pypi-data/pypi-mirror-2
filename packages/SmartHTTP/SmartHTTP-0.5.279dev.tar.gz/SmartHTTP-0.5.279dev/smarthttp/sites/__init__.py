# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites
    Site handlers
    Last changed on 2010-07-14 21:32:26+11:00 rev. 276:8c9f14045dfe by Dan Kluev <dan@kluev.name>

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


Site handlers
=============

:mod:`smarthttp.sites.manager`
:mod:`smarthttp.sites.arbitrary`

.. _smarthttp.sites-SiteHandler:

:class:`SiteHandler`
--------------------

Base class for site-handlers.
    Should not be subclassed directly, use :class:`SiteEngine` or :class:`SpecificSite` instead.
    

.. autoclass:: SiteHandler
    :members:
    :undoc-members:

.. _smarthttp.sites-SiteFunctionResult:

:class:`SiteFunctionResult`
---------------------------



.. autoclass:: SiteFunctionResult
    :members:
    :undoc-members:

.. _smarthttp.sites-SiteEngine:

:class:`SiteEngine`
-------------------

Base class for site-handlers, which provide interface to engine or some set of sites
    

.. autoclass:: SiteEngine
    :members:
    :undoc-members:

.. _smarthttp.sites-SpecificSite:

:class:`SpecificSite`
---------------------

Base class for site-handlers for specific sites.
    

.. autoclass:: SpecificSite
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from ..client import HTTPClient
import time
import re
from datetime import datetime
from ..exceptions import ParseException, ResultException, SmartHTTPException
from ..lib.containers import SmartDict, strdict
from ..urls import URL
from ..urls.maps import SmartMap, LocalMap
import logging

class SiteFunctionResult(object):
    data = None
    error = True
    error_text = u""
    error_code = 0
    resp = None
    def __init__(self, data=None, error=None, error_text=u"", error_code=0, resp=None):
        if not data is None and not error:
            self.data = data
            self.error = False
        elif error:
            self.error = True
            self.error_text = error_text
            self.error_code = error_code
        self.resp = resp

    def __bool__(self):
        return not self.error
    def __nonzero__(self):
        return not self.error
    
    def __getattribute__(self, item):
        if item.startswith('__') and item.endswith('__'):
            return object.__getattribute__(self, item)
        if item == 'data' and object.__getattribute__(self, 'error'):
            raise ResultException(self.error_text)
        return object.__getattribute__(self, item)
        """
        elif hasattr(self, item) or hasattr(object.__getattribute__(self, '__class__'), item):
            return object.__getattribute__(self, item)
        else:
            data = object.__getattribute__(self, 'data')
            return data.__getattribute__(item)
        """

    def __repr__(self):
        if type(self.data) == unicode:
            data = self.data.encode('utf-8')
        else:
            data = self.data
        return "<SiteResult(%s, %s)>" % (self.error and ('Error', self.error_text) or ('OK', data))


class SiteHandler(object):
    """Base class for site-handlers.
    Should not be subclassed directly, use :class:`SiteEngine` or :class:`SpecificSite` instead.
    """
    proto = 'http'
    delay = 0
    last_request = None
    base_path = None
    domain = None
    port   = 80
    dateformat = "%Y-%m-%d %H:%M:%S"
    map    = SmartMap()
    def __init__(self, client=None, log=None, delay=0, **kw):
        """All parameters are optional. It will create according objects with default settings if omitted.
        
        :param client: :class:`~smarthttp.client.HTTPClient` instance
        :param log: Logger instance
        :param delay: Sleep this many seconds between requests
        """
        self.delay = delay
        if not client and not log:
            log = logging.getLogger("smarthttp.sites.%s" % self.__class__.__name__)
        if not client:
            client = HTTPClient(logger=log)
        self.client = client
        if log:
            self.log = log
        elif self.client.log:
            self.log = self.client.log
        else:
            self.log = logging.getLogger(self.__class__.__name__)

    def url(self, route, params=None, **kw):
        """
        Generate :class:`~smarthttp.urls.URL` according to the site map
        :param route: Route name or url
        :param params: dict with params for the route
        :param kw: dict with params for the route
        :rtype: :class:`~smarthttp.urls.URL`
        .. todo:: Intergate direct urls with maps somehow
        """
        if '/' in route or ':' in route:
            url = route
        else:
            url = self.map.url(route, params, **kw)
        return URL(url)
        
    def load(self, route, params=None, **kw):
        """
        Compile URL and send request. Equivalent of self.request(self.url(route, params, **kw))
        :rtype: :class:`~smarthttp.http.HTTPResponse`
        """
        return self.request(self.url(route, params, **kw))
        
    def parse(self, route, params=None, **kw):
        """
        Load and parse page according to the site map.
        :rtype: :class:`~smarthttp.sites.SiteFunctionResult`

        .. todo:: 1. Add `parsers` param, 2. Allow HTTPResponse objects instead of Routes, 3. Error handling
        
        """
        resp = self.load(route, params=params, **kw)
        result  = SmartDict()
        parsers = self.map.get_parsers(route)
        for parser in parsers:
            subresult = parser(self, resp)
            result = result._merge(subresult.data)
        return self.ok(result)
            

    def request(self, url, **kw):
        """
        Send request to :class:`~smarthttp.client.HTTPClient`
        :param url: :class:`~smarthttp.urls.URL`
        :rtype: :class:`~smarthttp.http.HTTPResponse`
        """
        if not isinstance(url, URL):
            raise SmartHTTPException('url parameter should be instance of urls.URL')
        if self.delay and self.last_request:
            td = (datetime.now() - self.last_request).seconds
            if td < self.delay:
                sleep = self.delay - td
                self.log.info("Should sleep %s seconds before next request" % sleep)
                time.sleep(sleep)
        self.last_request = datetime.now()
        req = self.client.request(url, **kw)
        return req

    def error(self, error, code=0, resp=None):
        return SiteFunctionResult(error=True, error_text=error, error_code=code, resp=resp)

    def ok(self, data, resp=None):
        return SiteFunctionResult(data=data, error=False, resp=resp)

    def result(self, data, resp=None):
        return SiteFunctionResult(data=data, error=False, resp=resp)

    def date(self, datestr):
        """
        Return DateTime object from datestr according to dateformat (should be mapped to request and urllmap somehow)
        """
        return datetime.strptime(datestr, self.dateformat)

    def __repr__(self):
        return "<Site[{0.__class__.__name__}] @ {0.proto} {0.domain} {0.base_path}>".format(self)

class SpecificSite(SiteHandler):
    """Base class for site-handlers for specific sites.
    """
    def __init__(self, *args, **kw):
        """See :class:`SiteHandler` constructor for params.
        """
        SiteHandler.__init__(self, *args, **kw)
        if self.map:
            self.map = LocalMap(site=self, _map=self.map)


class SiteEngine(SiteHandler):
    """Base class for site-handlers, which provide interface to engine or some set of sites
    """
    def __init__(self, domain=None, port=80, base_path=None, url=None, *args, **kw):
        """
        :param domain: Domain on which site instance is installed.
        :param port: HTTP server port
        :param base_path: Path to installation root
        :param url: :class:`~smarthttp.urls.URL` or string which is used to get domain, port and base_path values.
        :param args: passed to :class:`SiteHandler` constructor.
        :param kw: passed to :class:`SiteHandler` constructor.
        """
        SiteHandler.__init__(self, *args, **kw)
        if url:
            if not isinstance(url, URL):
                url = URL(url)
            domain = url.hostname or domain
            if url.path or url.query:
                base_path = url.path
                if url.query:
                    base_path = "{0}?{1}".format(base_path, url.query)
            self.port = url.port or port
        self.domain = domain
        if base_path:
            if base_path[0] != '/':
                base_path = "/%s" % base_path
            if base_path[-1] == '/':
                base_path = base_path[:-1]
        self.base_path = base_path
        if self.map:
            self.map = LocalMap(site=self, _map=self.map)
