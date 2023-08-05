# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.urls
    URLs tools
    Last changed on 2010-07-20 15:31:20+11:00 rev. 279:0e18c726f36b by Dan Kluev <dan@kluev.name>

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


URLs tools
==========

.. _smarthttp.urls-URL:

:class:`URL`
------------


    .. todo:: 1) Add proper url bits editing and re-compiling 2) Add support for alternative param separators
    

.. autoclass:: URL
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

import urlparse as _urlparse
from urllib import quote, urlencode

class URL(object):
    """
    .. todo:: 1) Add proper url bits editing and re-compiling 2) Add support for alternative param separators
    """
    __slots__ = ['url', 'splitres', 'scheme', 'netloc', 'hostname', 'port', 'path', 'params', 'query']
    def __init__(self, url):
        splitres = _urlparse.urlsplit(url)
        if splitres.query:
            params = _urlparse.parse_qs(splitres.query, True)
        else:
            params = {}
        self.url = url
        self.splitres = splitres
        self.scheme = splitres.scheme
        self.netloc = splitres.netloc
        self.port   = splitres.port
        self.path   = splitres.path
        self.query  = splitres.query
        self.hostname = splitres.hostname
        self.params = params

    def geturl(self, *args, **kw):
        return self.splitres.geturl(*args, **kw)
    
    def __repr__(self):
        return "<URL({0.url})>".format(self)
