# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.jython.http
    HTTP implementation for Jython
    Last changed on Wed Apr 14 14:50:37 2010 +1100 rev. 111:5efdacc70dde by Dan Kluev <orion@ssorion.info>

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
"""

import logging
log = logging.getLogger(__name__)

class HTTPResult:
    pass

class HTTPError(HTTPResult):
    pass

def DoHTTPRequest(uri, referer=None, cookies=None, request="GET", data=[], connecttimeout=30, timeout=120, signals=False, logger=None, verbose=True,
        user_agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3",
        ):
    pass
