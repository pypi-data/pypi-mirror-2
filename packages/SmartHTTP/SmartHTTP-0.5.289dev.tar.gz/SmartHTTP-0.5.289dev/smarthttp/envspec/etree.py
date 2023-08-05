# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.etree
    ElementTree implementation
    Last changed on 2010-05-21 21:03:13+11:00 rev. 222:332abf0c0c9e by Dan Kluev <orion@ssorion.info>

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


ElementTree implementation
==========================
"""

__docformat__ = 'restructuredtext'

from . import interpreter
if interpreter == 'CPython':
    from .cpython import etree
elif interpreter == 'Jython':
    from .jython import etree
else:
    from .pure import etree

import types
ldict = locals()
for k, v in etree.__dict__.iteritems():
    if not k.startswith('__') or not k.endswith('__'):
        ldict[k] = v
