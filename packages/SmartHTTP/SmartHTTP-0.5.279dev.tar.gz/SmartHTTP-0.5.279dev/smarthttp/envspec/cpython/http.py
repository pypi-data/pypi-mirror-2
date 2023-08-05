# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.cpython.http
    cURL HTTP implementation
    Last changed on 2010-05-28 23:08:28+11:00 rev. 243:b5cb8d033b8f by Dan Kluev <dan@kluev.name>

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


cURL HTTP implementation
========================
"""
__docformat__ = 'restructuredtext'

import pycurl
from pycurl import *
from smarthttp.http import HTTPResponse, HTTPError
import StringIO
import logging
log = logging.getLogger(__name__)

library_name = 'libcurl'
library_version_full = version_info()
library_version = "libcurl/{1}".format(*library_version_full)

class HTTPResponseCurl(HTTPResponse):
    def __init__(self, c, data, headers):
        self.error = False
        self.data = data
        self.document = None
        self.date = c.getinfo(INFO_FILETIME)
        self.code = c.getinfo(HTTP_CODE)
        self.size = c.getinfo(CONTENT_LENGTH_DOWNLOAD)
        if len(self.data) > self.size:
            self.size = len(self.data)
        self.url  = c.getinfo(EFFECTIVE_URL)
        self.parse_header(headers)

class HTTPErrorCurl(HTTPError):
    def __init__(self, c, e):
        self.data = None
        self.cookies = None
        self.headers = None
        self.document = None
        self.type = None
        self.subtype = None
        self.error = True
        self.error_text = e
        self.date = c.getinfo(INFO_FILETIME)
        self.code = c.getinfo(HTTP_CODE)
        self.size = c.getinfo(CONTENT_LENGTH_DOWNLOAD)
        self.url  = c.getinfo(EFFECTIVE_URL)

def DoHTTPRequest(request, connecttimeout=30, timeout=120, signals=False, logger=None, verbose=True):
    if not logger:
        logger = log
    c = Curl()
    d = StringIO.StringIO()
    h = StringIO.StringIO()
    c.setopt(URL, str(request.url))
    if request.data:
        if type(request.data) == dict:
            data_list = []
            for k, v in request.data.iteritems():
                if type(v) == unicode:
                    v = v.encode('utf-8')
                data_list.append((k, v))
        else:
            data_list = request.data
        c.setopt(POST, 1)
        c.setopt(HTTPPOST, data_list)
        request.method = "POST"
    elif request.method == "GET":
        c.setopt(HTTPGET, 1)
    elif request.method == "HEAD":
        c.setopt(NOBODY, 1)
    else:
        c.setopt(POST, 1)
    c.setopt(WRITEFUNCTION, d.write)
    c.setopt(HEADERFUNCTION, h.write)
    c.setopt(CONNECTTIMEOUT, connecttimeout)
    c.setopt(TIMEOUT, timeout)
    c.setopt(OPT_FILETIME, 1)
    c.setopt(ENCODING, "")
    c.setopt(FOLLOWLOCATION, 0)
    if not signals:
        c.setopt(NOSIGNAL, 1)
    if request.referer:
        c.setopt(REFERER, str(request.referer))
    else:
        c.setopt(REFERER, str(request.url))
    cookie_str = ""
    if request.cookies:
        for k, v in request.cookies.iteritems():
            cookie_str += "%s=%s; " % (k, v)
    c.setopt(COOKIE, str(cookie_str))
    c.setopt(USERAGENT, str(request.user_agent))
    if verbose:
        logger.debug("{0}, data {0.data}, cookies {0.cookies}".format(request))
    else:
        logger.debug(request)
    try:
        c.perform()
        r = HTTPResponseCurl(c, d.getvalue(), h.getvalue())
        logger.debug("Finished, code %s, %s bytes" % (r.code, len(r.data)))
    except pycurl.error, e:
        logger.warn(e)
        r = HTTPErrorCurl(c, e)
    c.close()
    return r

