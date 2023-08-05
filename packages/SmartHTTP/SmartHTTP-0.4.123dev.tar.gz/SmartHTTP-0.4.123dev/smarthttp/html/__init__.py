# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.html
    Implementation of DOM parser, tree and related utilities
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
from lxml import etree
import StringIO
import logging
log = logging.getLogger(__name__)
html_parser = etree.HTMLParser()

class DomElement(etree.ElementBase):
    pass

class HTMLDocument(etree._ElementTree):
    request = None
    def __init__(self, request=None):
        etree._ElementTree.__init__(self)
        if request:
            self.request = request
            self.parse(StringIO.StringIO(request.data), base_url=request.url)
            
    def parse(self, data, parser=None, lookup=None, base_url=None):
        if not lookup:
            lookup = etree.ElementDefaultClassLookup(element=DomElement)
            
        if not parser:
            parser = etree.HTMLParser()
            parser.set_element_class_lookup(lookup)
            
        etree._ElementTree.parse(self, data, parser=parser, base_url=base_url)
        
def GetNextTag(el, tag, skip=0):
    tag = tag.lower()
    if skip:
        r = el.getnext()
    else:
        r = el
    if not r.tag or r.tag.lower() != tag:
        while (r.getnext() != None) and not (r.getnext().tag and r.getnext().tag.lower() == tag):
            r = r.getnext()
        if r.getnext() != None:
            r = r.getnext()
    if r.tag and r.tag.lower() == tag:
        return r
    else:
        return None
    
def GetPreviousTag(el, tag, skip=0):
    tag = tag.lower()
    if skip:
        r = el.getprevious()
    else:
        r = el
    if not r.tag or r.tag.lower() != tag:
        while (r.getprevious() != None) and not (r.getprevious().tag and r.getprevious().tag.lower() == tag):
            r = r.getprevious()
        if r.getprevious() != None:
            r = r.getprevious()
    if r.tag and r.tag.lower() == tag:
        return r
    else:
        return None

def GetTextBetween(text, start, end):
    start_pos = text.find(start)
    end_pos = text.find(end)
    if start_pos >= 0 and end_pos >= 0:
        start_pos += len(start)
        return text[start_pos:end_pos]
    else:
        return None

def GetDOM(rawhtml):
    document = etree.parse(StringIO.StringIO(rawhtml), html_parser)
    return document

def GetPlainText(node=None, text=u'', rawhtml=u''):
    if rawhtml and node is None:
        node = GetDOM(rawhtml).getroot()
    if node.tag != etree.Comment and node.text:
        if text and text[-1] != ' ':
            text += ' '
        text += node.text
    if node.tag != etree.Comment and len(node)>0:
        for n in node:
            text = GetPlainText(n, text)
    if node.tail:
        if text and text[-1] != ' ':
            text += ' '        
        text += node.tail
    return text


def ForcedEncoding(text, enc):
    return u''.join(map(lambda x:x.decode(enc), map(chr, filter(lambda x:x < 256, map(ord, text)))))
