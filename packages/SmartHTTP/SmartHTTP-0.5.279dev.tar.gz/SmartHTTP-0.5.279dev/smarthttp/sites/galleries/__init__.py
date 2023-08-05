# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries
    Galleries site-handlers
    Last changed on 2010-07-14 21:32:49+11:00 rev. 277:8cb513eeb9c1 by Dan Kluev <dan@kluev.name>

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


Galleries site-handlers
=======================

.. _smarthttp.sites.galleries-Image:

:class:`Image`
--------------



.. autoclass:: Image
    :members:
    :undoc-members:

.. _smarthttp.sites.galleries-Tag:

:class:`Tag`
------------



.. autoclass:: Tag
    :members:
    :undoc-members:

.. _smarthttp.sites.galleries-User:

:class:`User`
-------------



.. autoclass:: User
    :members:
    :undoc-members:

.. _smarthttp.sites.galleries-Gallery:

:class:`Gallery`
----------------


    Gallery mix-in.
    Gallery typically has albums or tags. 
    Each album/tag is treated as list of pictures
    

.. autoclass:: Gallery
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from .. import *

class Gallery(object):
    """
    Gallery mix-in.
    Gallery typically has albums or tags. 
    Each album/tag is treated as list of pictures
    """
    def get_image(self):
        """
        Load image page
        """
        raise NotImplemented(self)
        
class Tag(object):
    tag = None
    count = 0
    types = None
    name_ru = None
    name_jp = None
    def __init__(self, tag=None, count=0, types=None, name_ru=None, name_jp=None):
        if type(tag) == str:
            tag = unicode(tag)
        elif type(tag) != unicode:
            raise ValueError(u"Tag should be string")
        self.tag = tag
        if type(count) != int:
            count = int(count)
        self.count = count
        if type(types) != list and type(types) != set:
            types = []
        self.types = types
        self.name_ru = name_ru
        self.name_jp = name_jp

class User(object):
    id   = None
    name = None
    avatar = None
    homesite = None

    def __init__(self, id=None, name=None, avatar=None, homesite=None):
        self.id = id
        self.name = name
        self.avatar = avatar
        self.homesite = homesite

    def __repr__(self):
        return "<User(id={0.id}, name={1})>".format(self, self.name.encode('utf-8'))

class Image(object):
    id     = None
    title  = None
    author = None
    
