# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.xml
    XML documents
    Last changed on 2010-05-21 22:01:28+11:00 rev. 224:7a4996b6c7f0 by Dan Kluev <orion@ssorion.info>

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


XML documents
=============

.. _smarthttp.xml-XMLDocument:

:class:`XMLDocument`
--------------------



.. autoclass:: XMLDocument
    :members:
    :undoc-members:

.. _smarthttp.xml-XMLElement:

:class:`XMLElement`
-------------------



.. autoclass:: XMLElement
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from .asserts import XMLAssertMixIn
from .envspec.etree import ElementTree, ElementBase, XMLParser, ElementDefaultClassLookup
from StringIO import StringIO

import logging
log = logging.getLogger(__name__)

class XMLDocument(ElementTree, XMLAssertMixIn):
    request = None
    def __init__(self, request=None):
        ElementTree.__init__(self)
        if request:
            self.request = request
            self.parse(StringIO(request.data), base_url=request.url)
            
    def parse(self, data, parser=None, lookup=None, base_url=None):
        if not lookup:
            lookup = ElementDefaultClassLookup(element=XMLElement)
            
        if not parser:
            parser = XMLParser()
            parser.set_element_class_lookup(lookup)
            
        ElementTree.parse(self, data, parser=parser, base_url=base_url)

class XMLElement(ElementBase, XMLAssertMixIn):
    pass
