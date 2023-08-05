# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.cpython.etree
    lxml ElementTree wrapper
    Last changed on 2010-07-14 21:30:51+11:00 rev. 274:5e77d6f1487d by Dan Kluev <dan@kluev.name>

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


lxml ElementTree wrapper
========================
"""
__docformat__ = 'restructuredtext'
from StringIO import StringIO
from lxml import etree 
f_filter = __builtins__.get('filter')

class LXMLETreeMixIn(object):
    def xpath(self, path, filter=None, classes=None, **kw):
        res = self._cls.xpath(self, path)
        if filter:
            res = f_filter(filter, res)
        if classes:
            if type(classes) == str or type(classes) == unicode:
                res = f_filter(lambda x: classes in x.classes, res)
        return res

    def xpath_one(self, path):
        res = self._cls.xpath(self, path)
        if res:
            return res[0]
        else:
            return None

    def tounicode(self, *args, **kw):
        return etree.tounicode(self, *args, **kw)
        

class ElementTree(LXMLETreeMixIn, etree._ElementTree):
    _cls = etree._ElementTree
    def parse_html(self, html):
        htmltree = etree.parse(StringIO(html), parser=self._parser, base_url=self._base_url)
        return htmltree

 
class ElementBase(LXMLETreeMixIn, etree.ElementBase):
    _cls = etree.ElementBase        

HTMLParser = etree.HTMLParser
HTML5Parser = HTMLParser
XMLParser  = etree.XMLParser
CustomElementClassLookup = etree.CustomElementClassLookup
ElementDefaultClassLookup = etree.ElementDefaultClassLookup
