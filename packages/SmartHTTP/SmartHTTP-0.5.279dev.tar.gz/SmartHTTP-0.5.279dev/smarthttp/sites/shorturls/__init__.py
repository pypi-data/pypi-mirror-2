# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.shorturls
    Url-shortener site-handlers
    Last changed on 2010-05-16 01:36:04+11:00 rev. 180:e516627a0283 by Dan Kluev <orion@ssorion.info>

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


Url-shortener site-handlers
===========================

List of url-shortening services:
http://code.google.com/p/shortenurl/wiki/URLShorteningServices

.. _smarthttp.sites.shorturls-UrlShortener:

:class:`UrlShortener`
---------------------


    Handler for typical url-shortening service, which just returns redirect by http header or meta tag or -simple- js
    

.. autoclass:: UrlShortener
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from .. import *

class UrlShortener(SiteEngine):
    """
    Handler for typical url-shortening service, which just returns redirect by http header or meta tag or -simple- js
    """
    pass
