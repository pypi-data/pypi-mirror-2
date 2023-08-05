# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.html.microformats
    Microformats parsing
    Last changed on 2010-06-21 08:51:59+11:00 rev. 258:51c08f6c6545 by Dan Kluev <dan@kluev.name>

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


Microformats parsing
====================

.. todo: Rewrite with separate class for each property.
    Keep in mind that there are singular and plural properties. Second ones can have multiple values.
    Each property may parse different html attributes in different ways and validate it.
    There should be some way to easily see what properties we found.
    Some hCards put presentation elements around property elements.

.. _smarthttp.html.microformats-MicroformatProperty:

:class:`MicroformatProperty`
----------------------------

Objects which hold retrieved properties.

.. autoclass:: MicroformatProperty
    :members:
    :undoc-members:

.. _smarthttp.html.microformats-MicroformatObject:

:class:`MicroformatObject`
--------------------------

Generic HTML microformat parser.

    Reference: http://microformats.org/
    
    

.. autoclass:: MicroformatObject
    :members:
    :undoc-members:

.. _smarthttp.html.microformats-hCard:

:class:`hCard`
--------------

HTML representation of vCard.
    
    Reference: http://microformats.org/wiki/hcard#Format
    
    

.. autoclass:: hCard
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

class MicroformatObject(object):
    """Generic HTML microformat parser.

    Reference: http://microformats.org/
    
    """
    def make_property(self, name, value):
        return MicroformatProperty.make(self.__class__.__name__, name, value)
    
    def set_attrs(self):
        for name, value in self.tree.iteritems():
            self.__setattr__(name.replace('-', '_'), self.make_property(name, value))
            
    def parse(self, parent=None, element=None):
        if not parent:
            parent = (self, self.tree)
        tree = parent[1]
        node = parent[0]
        if element is None:
            element = self.root
        for child in element.getchildren():
            for cls in child.classes:
                if cls in tree:
                    pname = cls.replace('-', '_')
                    if tree[cls]:
                        self.parse((node.__getattribute__(pname), tree[cls]), child)
                    else:
                        node.__setattr__(pname, child.plaintext)
    

class MicroformatProperty(object):
    """Objects which hold retrieved properties."""
    mfname = None
    name   = None
    
    @classmethod
    def make(cls, mfname, name, tree):
        if not tree:
            return None
        else:
            return cls(mfname, name, tree)
        
    def __init__(self, mfname, pname, tree):
        """Create property tree from dict tree
        """
        self.mfname = mfname
        self.name   = pname
        for name, value in tree.iteritems():
            if '-' in name:
                name = name.replace('-', '_')
            self.__setattr__(name, MicroformatProperty.make(mfname, u"{0}.{1}".format(pname, name), value))

    def __repr__(self):
        return u"<{0.mfname}:{0.name}>".format(self)
        
            

class hCard(MicroformatObject):
    """HTML representation of vCard.
    
    Reference: http://microformats.org/wiki/hcard#Format
    
    """
    root = None
    tree = {'fn':{},
            'n':{'family-name':{},
                 'given-name':{},
                 'additional-name':{},
                 'honorific-prefix':{},
                 'honorific-suffix':{}},
            'adr':{'post-office-box':{},
                   'extended-address':{},
                   'street-address':{},
                   'locality':{},
                   'region':{},
                   'postal-code':{},
                   'country-name':{},
                   'type':{},
                   'value':{}},
            'agent':{},
            'bday':{},
            'category':{},
            'class':{},
            'email':{'type':{},
                     'value':{}},
            'geo':{'latitude':{},
                   'longitude':{}},
            'key':{},
            'label':{},
            'logo':{},
            'mailer':{},
            'nickname':{},
            'note':{},
            'org':{'organization-name':{},
                   'organization-unit':{}},
            'photo':{},
            'rev':{},
            'role':{},
            'sort-string':{},
            'sound':{},
            'tel':{'type':{},
                    'value':{}},
            'title':{},
            'tz':{},
            'uid':{},
            'url':{},
            'meta-type':{},
        }
    def __init__(self, root):
        """Parses hCard data from html tree.

        :param root: HTML tree element with 'vcard' class.
        """
        self.root = root
        self.set_attrs()
        self.parse()

    def __repr__(self):
        return "<hCard>"
