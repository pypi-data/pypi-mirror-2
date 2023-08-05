# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.jython.http
    Jython HTTP implementation
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


Jython HTTP implementation
==========================
"""
__docformat__ = 'restructuredtext'

from smarthttp.http import HTTPResponse, HTTPError
import logging
log = logging.getLogger(__name__)

library_name = 'jython'
library_version = "Jython/stub"
library_version_full = library_version

def DoHTTPRequest(request, connecttimeout=30, timeout=120, signals=False, logger=None, verbose=True):
    if not logger:
        logger = log
