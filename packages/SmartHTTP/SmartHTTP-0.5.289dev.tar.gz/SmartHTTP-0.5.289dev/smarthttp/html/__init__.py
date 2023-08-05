# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.html
    HTML Documents
    Last changed on 2010-06-21 08:49:20+11:00 rev. 257:1a96ab18ab70 by Dan Kluev <dan@kluev.name>

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


HTML Documents
==============

.. _smarthttp.html-HTMLDocument:

:class:`HTMLDocument`
---------------------



.. autoclass:: HTMLDocument
    :members:
    :undoc-members:

.. _smarthttp.html-DomElement:

:class:`DomElement`
-------------------



.. autoclass:: DomElement
    :members:
    :undoc-members:

.. _smarthttp.html-TableElement:

:class:`TableElement`
---------------------


    Represents HTML <table/> element.
    Reference: http://www.w3.org/TR/html401/struct/tables.html#h-11.2
    

.. autoclass:: TableElement
    :members:
    :undoc-members:

.. _smarthttp.html-FormElement:

:class:`FormElement`
--------------------



.. autoclass:: FormElement
    :members:
    :undoc-members:

.. _smarthttp.html-LinkElement:

:class:`LinkElement`
--------------------



.. autoclass:: LinkElement
    :members:
    :undoc-members:

.. _smarthttp.html-DomElementLookup:

:class:`DomElementLookup`
-------------------------



.. autoclass:: DomElementLookup
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from ..envspec.etree import ElementTree, ElementBase, HTMLParser, HTML5Parser, CustomElementClassLookup
from ..envspec.js import JSEnabled, JSEngine, JSClass
from .js import JSWindow
from ..urls import URL
from ..exceptions import SmartHTTPException, HTMLSyntaxError
from ..asserts import XMLAssertMixIn
from StringIO import StringIO
import logging
log = logging.getLogger(__name__)

class HTMLDocument(ElementTree, XMLAssertMixIn):
    request = None
    _body   = None
    _parser = None
    _base_url = None
    _js_engine = None
    _js_context = None
    _js_evaled = False
    _writes = None
    def __init__(self, request=None, html5=False):
        ElementTree.__init__(self)
        if request:
            self.request = request
            self.parse(StringIO(request.data), base_url=request.url)
        self._writes = []
        self._body   = self.find('body')
            
    def parse(self, data, parser=None, lookup=None, base_url=None):
        if not lookup:
            lookup = DomElementLookup()            
        if not parser:
            parser = HTMLParser()
            parser.set_element_class_lookup(lookup)
        self._parser = parser
        self._base_url = base_url
        try:
            ElementTree.parse(self, data, parser=parser, base_url=base_url)
        except Exception, e:
            raise HTMLSyntaxError(str(e))
        if self.getroot() is None:
            raise HTMLSyntaxError("Invalid HTML - no root node.")
    
    @property
    def forms(self):
        return self.xpath('//form')

    def eval_js(self, client=None, eval_internal=True, eval_external=False, js=None):
        """Evaluate JS on the page if possible.
        
        :param eval_internal: Evaluate JS in the page itself if True
        :param eval_external: Evaluate JS in separate files linked from the page
        :param js: Evaluate this as JS in page context
        :rtype: If `js` is given, returns result. Otherwise returns True on success and False on fail.
        """
        if not JSEnabled:
            return False
        if not self._js_context:
            if not client:
                client = self.request.client
            self._js_context = JSWindow(self, client)
        if not self._js_engine:
            self._js_engine  = JSEngine(self._js_context)

        result = True
        if not self._js_evaled and (eval_internal or eval_external):
            scripts = self.xpath("//script")
            for script in scripts:
                src = script.get('src')
                if src:
                    if eval_external:
                        pass
                elif eval_internal:
                    self._js_context._caller_node = script
                    self._js_engine.eval(script.text)                    

        if js:
            result = self._js_engine.eval(js)
        return result    
            
    @property
    def tables(self):
        return self.xpath('//table')

    def append_html(self, html):
        htmltree = self.parse_html(html)
        self._body.extend(htmltree.find('body').getchildren())

    def insert_html(self, element, html):
        htmltree = self.parse_html(html)
        for child in htmltree.find('body').getchildren()[::-1]:
            element.addnext(child)
    

class DomElementLookup(CustomElementClassLookup):
    def lookup(self, node_type, document, namespace, name):
        if name in LookupMap:
            return LookupMap[name]
        else:
            return DomElement
        

class DomElement(ElementBase, XMLAssertMixIn):
    @property
    def id(self):
        return self.get('id')
        
    @property
    def class_(self):
        return self.get('class')

    @property    
    def classes(self):
        cls = self.class_
        if cls:
            return cls.split()
        else:
            return []
    
    def __repr__(self):
        id = self.id
        id = id and "#{0}".format(id) or ''
        cls = self.class_
        cls = cls and ".{0}".format(cls) or ''
        return "<{0.__class__.__name__} {0.tag}{1}{2}>".format(self, id, cls)
        
    @property
    def plaintext(self):
        text = []
        if self.text:
            text.append(self.text)
        for child in self.getchildren():
            child_text = child.plaintext
            if child_text:
                text.append(child_text)
            if child.tail:
                text.append(child.tail)
        return u''.join(text)
        
class FormElement(DomElement):
    @property
    def fields(self):
        inputs = self.xpath('.//input')
        selects = self.xpath('.//select')

class TableElement(DomElement):
    """
    Represents HTML <table/> element.
    Reference: http://www.w3.org/TR/html401/struct/tables.html#h-11.2
    """
    _headers = None
    @property
    def tbody(self):
        """Get <tbody/> if it exists, or return itself otherwise.
        
        :rtype: <tbody/> or <table/> element
        """
        el = self.xpath('./tbody')
        if el:
            return el[0]
        else:
            return self
        
    @property
    def headers(self):
        """Get list of table headers
        
        :rtype: List of headers
        
        .. todo:: Take scope and rowspan into account
        .. todo:: Should consider <tr><th></th></tr> as <thead>
        
        """
        if self._headers:
            return self._headers
        cols = []
        header = self.xpath('./thead')
        if header:
            cols = header.xpath('./tr[1]/th')
            if not cols:
                cols = header.xpath('./tr[1]/td')
        else:
            tbody = self.tbody
            cols  = tbody.xpath('./tr[1]/th')
            if not cols:
                tbody.xpath('./tr[1]/td')
        res = []
        if cols:
            for col in cols:
                res.append(col.plaintext.strip())
            self._headers = res
        return res

    def rows(self, cols=None, dicts=False):
        """
        :param col: List of indexes or names of columns to return. Returns all columns if omitted.
        :param dicts: If `True`, return rows as dicts, with keys being column names from headers, otherwise return lists
        :rtype: Iterator which returns rows one by one.
        
        .. todo:: Take scope and colspan into account
        """
        if cols or dicts:
            headers = self.headers
        if cols:
            cols_res = []
            headers = self.headers
            for colname in cols:
                if colname in headers:
                    idx = headers.index(colname)
                elif type(colname) == int:
                    idx = colname
                else:
                    raise SmartHTTPException("Unknown column {0} for {1}, available columns: {2}".format(colname, self, headers))
                cols_res.append(idx)
            cols = cols_res

        tbody = self.tbody
        for tr in tbody.xpath('./tr'):
            tds = []
            for td in tr.xpath('./td'):
                colspan = int(td.get('colspan', '1'))
                for i in range(colspan):
                    tds.append(td)
            if not tds:
                continue
            if dicts:
                row = {}
                if cols:
                    for idx in cols:
                        row[headers[idx]] = tds[idx]
                else:
                    for idx in range(len(headers)):
                        row[headers[idx]] = tds[idx]
            else:
                if cols:
                    row = []
                    for idx in cols:
                        row.append(tds[idx])
                else:
                    row = tds
            yield row
                
    
class LinkElement(DomElement):
    @property
    def href(self):
        return URL(self.get('href', ''))

LookupMap = {'form':FormElement,
             'table':TableElement,
             'a':LinkElement,
             }

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
