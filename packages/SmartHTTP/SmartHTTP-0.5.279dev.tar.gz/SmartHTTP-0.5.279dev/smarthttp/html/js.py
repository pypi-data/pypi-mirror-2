# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.html.js
    HTML DOM JS API
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


HTML DOM JS API
===============

References:
https://developer.mozilla.org/en/Gecko_DOM_Reference
http://www.whatwg.org/specs/web-apps/current-work/multipage/index.html#auto-toc-3
http://www.w3.org/TR/2004/REC-DOM-Level-3-Core-20040407/idl-definitions.html

.. _smarthttp.html.js-JSDocument:

:class:`JSDocument`
-------------------


    http://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-1006298752
    http://www.w3.org/TR/DOM-Level-2-Core/core.html#i-Document
    http://dev.w3.org/html5/spec/dom.html#documents-in-the-dom
    

.. autoclass:: JSDocument
    :members:
    :undoc-members:

.. _smarthttp.html.js-JSWindow:

:class:`JSWindow`
-----------------


    http://dev.w3.org/html5/spec/browsers.html#the-window-object
    

.. autoclass:: JSWindow
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from ..envspec.js import JSClass

class JSWindow(JSClass):
    """
    http://dev.w3.org/html5/spec/browsers.html#the-window-object
    """
    # Internal attributes
    _document = None
    _document_obj = None
    _client   = None
    _caller_node = None
    
    # DOM
    name = None
    location = None
    history = None
    undoManager = None
    locationbar = None
    menubar = None
    personalbar = None
    scrollbars = None
    statusbar = None
    toolbar = None
    frames = None
    length = None
    top    = None
    opener = None
    parent = None
    frameElement = None
    navigator = None
    applicationCache = None
    
    def __init__(self, document, client):
        JSClass.__init__(self)
        self._document = document
        self._client   = client

    @property
    def window(self):
        return self

    @property
    def document(self):
        if not self._document_obj:
            self._document_obj = JSDocument(self._document, self)
        return self._document_obj

    def getSelection(self):
        pass

    def open(self, *args):
        """
        WindowProxy open(in optional DOMString url, in optional DOMString target, in optional DOMString features, in optional DOMString replace);
        """
        pass
    
    def close(self):
        pass

    def stop(self):
        pass

    def focus(self):
        pass

    def blur(self):
        pass

    def alert(self, message):
        pass
    
    def confirm(self, message):
        return True

    def prompt(self, message, default=None):
        """
        DOMString prompt(in DOMString message, in optional DOMString default);
        """
        return default

    """
    print is reserved word, cannot define it directly, needs some hacking.
    def print(self):
        pass
    """
    
class JSDocument(JSClass):
    """
    http://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-1006298752
    http://www.w3.org/TR/DOM-Level-2-Core/core.html#i-Document
    http://dev.w3.org/html5/spec/dom.html#documents-in-the-dom
    """
    # Internal attributes
    _document = None

    # DOM 
    window = None
    title  = None
    referrer = None
    domain = None
    URL = None
    body = None
    images = None
    applets = None
    links  = None
    forms = None
    anchors = None
    cookie = None
    doctype = None
    implementation = None
    documentElement = None
    def __init__(self, document, window):
        JSClass.__init__(self)
        self._document = document
        self.window = window

    def write(self, markup):
        """
        Should write markup right where <script> tag is.
        """
        if not self.window._caller_node is None:
            self._document.insert_html(self.window._caller_node, markup)
        else:
            self._document.append_html(markup)

    writeln = write

    def getElementsByName(self, name):
        """
        NodeList           getElementsByName(in DOMString elementName);
        """
        return []

    def createElement(self, tagName):
        """
        Element            createElement(in DOMString tagName)
        """
    def createDocumentFragment(self):
        pass
    def createTextNode(self, data):
        """
        Text               createTextNode(in DOMString data);
        """
    def createComment(self, data):
        """
        Comment            createComment(in DOMString data);
        """
    def createCDATASection(self, data):
        """
        CDATASection       createCDATASection(in DOMString data)
        """
    def createProcessingInstruction(self, target, data):
        """
        ProcessingInstruction createProcessingInstruction(in DOMString target, in DOMString data)
        """
    def createAttribute(self, name):
        """
        Attr               createAttribute(in DOMString name)
        """
    def createEntityReference(self, name):
        """
        EntityReference    createEntityReference(in DOMString name)
        """
    def getElementsByTagName(self, tagname):
        """
        NodeList           getElementsByTagName(in DOMString tagname);
        """
    def importNode(self, importedNode, deep):
        """
        Node               importNode(in Node importedNode, in boolean deep)
        """
    def createElementNS(self, namespaceURI, qualifiedName):
        """
        Element            createElementNS(in DOMString namespaceURI, in DOMString qualifiedName)
        """
    def createAttributeNS(self, namespaceURI, qualifiedName):
        """
        Attr               createAttributeNS(in DOMString namespaceURI, in DOMString qualifiedName)
        """
    def getElementsByTagNameNS(self, namespaceURI, localName):
        """
        NodeList           getElementsByTagNameNS(in DOMString namespaceURI, in DOMString localName);
        """
    def getElementById(self, elementId):
        """
        Element            getElementById(in DOMString elementId);
        """

    def open(self):
        pass

    def close(self):
        pass

