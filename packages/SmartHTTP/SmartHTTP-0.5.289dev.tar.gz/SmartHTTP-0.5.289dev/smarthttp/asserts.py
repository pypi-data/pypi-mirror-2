# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.asserts
    Asserts
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


Asserts
=======

.. _smarthttp.asserts-ResponseAssertMixIn:

:class:`ResponseAssertMixIn`
----------------------------


    This mix-in is inherited by :class:`smarthttp.http.HTTPResponse` for code/type/preparse validations
    

.. autoclass:: ResponseAssertMixIn
    :members:
    :undoc-members:

.. _smarthttp.asserts-XMLAssertMixIn:

:class:`XMLAssertMixIn`
-----------------------


    This mix-in should be inherited by any class, which represents XML tree or node
    

.. autoclass:: XMLAssertMixIn
    :members:
    :undoc-members:

.. _smarthttp.asserts-DictAssertMixIn:

:class:`DictAssertMixIn`
------------------------


    This mix-in is inherited by SmartDict for validations
    

.. autoclass:: DictAssertMixIn
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from .exceptions import ParseException, XPathException, HTTPException, HTMLException, KeyException, ResultException, SmartHTTPException

class ResponseAssertMixIn(object):
    """
    This mix-in is inherited by :class:`smarthttp.http.HTTPResponse` for code/type/preparse validations
    """
    def assertHTTPOK(self):
        if self.error:
            raise HTTPException(u"HTTP Error")
        if self.code != 200:
            raise HTTPException(u"HTTP code %s" % self.code)
        return True

    def assertHTML(self):
        self.assertHTTPOK()
        try:
            document = self.html
        except Exception, e:
            raise ParseException(str(e))
        return document

    def assertJSON(self):
        self.assertHTTPOK()
        try:
            document = self.json
        except Exception, e:
            raise ParseException(str(e))
        return document
        
    def assertXML(self):
        self.assertHTTPOK()
        try:
            document = self.xml
        except Exception, e:
            raise ParseException(str(e))
        return document

class DictAssertMixIn(object):
    """
    This mix-in is inherited by SmartDict for validations
    """
    def assertKey(self, key):
        if dict.__contains__(self, key):
            return self.__getitem__(key)
        else:
            raise KeyException(u"Key {0} is missing.".format(key))

class XMLAssertMixIn(object):
    """
    This mix-in should be inherited by any class, which represents XML tree or node
    """
    def assertXPath(self, path, count=1, strict=False, **kw):
        res = self.xpath(path, **kw)
        if not res:
            raise XPathException(u"{0} did not match anything.".format(path))
        elif strict and len(res) != count:
            raise XPathException(u"{0} matched {1} instead of {2}.".format(path, len(res), count))
        elif not strict and len(res) < count:
            raise XPathException(u"{0} matched {1} which is less than {2}.".format(path, len(res), count))
        return res
        
    def assertXPathOne(self, path, **kw):
        res = self.assertXPath(path, count=1, strict=True, **kw)
        return res[0]

