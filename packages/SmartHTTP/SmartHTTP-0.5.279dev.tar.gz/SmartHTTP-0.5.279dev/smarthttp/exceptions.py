# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.exceptions
    SmartHTTP exceptions.
    Last changed on 2010-06-21 08:49:20+11:00 rev. 257:1a96ab18ab70 by Dan Kluev <dan@kluev.name>

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
class SmartHTTPException(Exception):
    pass

class ParseException(SmartHTTPException):
    pass
class XPathException(ParseException):
    pass
class HTTPException(ParseException):
    pass
class HTMLException(ParseException):
    pass
class KeyException(ParseException):
    pass

class ResultException(SmartHTTPException):
    pass

class NotImplemented(SmartHTTPException):
    def __init__(self, inst, *args, **kw):
        SmartHTTPException.__init__(self, *args, **kw)

class DocumentError(SmartHTTPException):
    pass

class HTMLSyntaxError(DocumentError):
    pass

class XMLSyntaxError(DocumentError):
    pass
