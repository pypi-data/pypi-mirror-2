# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.client
    HTTP Client
    Last changed on 2010-06-21 10:31:06+11:00 rev. 261:a326eeebfba7 by Dan Kluev <dan@kluev.name>

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


HTTP Client
===========

.. _smarthttp.client-HTTPClient:

:class:`HTTPClient`
-------------------


    HTTP Client object which abstracts all http-related libraries.
    

.. autoclass:: HTTPClient
    :members:
    :undoc-members:

"""
__docformat__ = 'reStructuredText'

import os
import random
import logging
from cookielib import CookieJar
from ..urls import URL
from ..http import HTTPRequest
from ..envspec.http import DoHTTPRequest
from .browsers import all_browsers, SmartHTTP as SmartHTTPBrowser
from .platforms import all_platforms, actual_platform
log = logging.getLogger(__name__)

class HTTPClient(object):
    """
    HTTP Client object which abstracts all http-related libraries.
    """
    retry = 5
    timeout = 120
    cookiejar = None
    def __init__(self, thread=None, logger=None, ua=None, mobile=False, retry=5):
        """
        All parameters are optional.

        :param thread: thread which use this client.
        :type  thread: :class:`threading.Thread` or `None`
        :param logger: logger which will receive log events. If None, uses logging.getLogger(__name__)
        :type  logger: :class:`logging.Logger` or `None`
        :param ua: User-agent. Can be `True` for library proper user-agent, string, or `False`/`None` to generate random, browser-like UA.
        :param mobile: if `True`, pretend to be a mobile browser
        :param retry: Amount of attempts before raising exception on request. -1 for unlimited amount.
        """
        global log
        self.thread = thread
        if logger:
            self.log = logger
        elif self.thread:
            self.log = logging.getLogger("%s.client" % (thread.name))
        else:
            self.log = logging.getLogger(__name__)
        self.cookiejar = CookieJar()
        if ua:
            self.platform = actual_platform
            self.browser = SmartHTTPBrowser(platform=self.platform)
            if ua is True:
                self.user_agent = self.browser.user_agent
            else:
                self.browser.user_agent = ua
                self.user_agent = ua
        else:
            self.platform = random.choice(all_platforms)()
            self.browser  = random.choice(all_browsers)(platform=self.platform)
            self.user_agent = self.browser.user_agent
        self.history = []
        self.retry = retry

    def load(self, site):
        site.load(self)

    def request(self, url, data=None, referer=None, method="GET", retry=None, **kw):
        """
        Send http request with this client
        
        :param url: :class:`~smarthttp.urls.URL` or string.
        :param data: POST request data
        :param method: HTTP method
        :param referer: HTTP Referer header
        :param retry: Number of retry attempts before returning failure
        :param kw: All other keywords are passed to underlying http library
        :rtype: :class:`~smarthttp.http.HTTPResponse` instance
        """
        if not isinstance(url, URL):
            url = URL(url)
        if not retry:
            retry = self.retry
        if not 'timeout' in kw:
            kw['timeout'] = self.timeout
        if not referer:
            if self.history:
                referer = self.history[-1]['url']
            else:
                referer = url
        if not isinstance(referer, URL):
            referer = URL(referer)

        req = HTTPRequest(url, data=data, referer=referer, method=method, user_agent=self.user_agent)
        req.set_cookies(self.cookiejar)
        
        attempt = 1
        while attempt < retry or retry == -1:
            if self.thread:
                self.thread.check_kill()
            resp = DoHTTPRequest(req, logger=self.log, **kw)
            if self.thread:
                self.thread.check_kill()
            if resp.error:
                self.log.debug("Attempt %s failed for url %s" % (attempt, url))
                attempt += 1
            else:
                break
        self.history.append({'url':url})
        if not resp.error:
            self.cookiejar.extract_cookies(resp, req)
        resp.client = self
        return resp
