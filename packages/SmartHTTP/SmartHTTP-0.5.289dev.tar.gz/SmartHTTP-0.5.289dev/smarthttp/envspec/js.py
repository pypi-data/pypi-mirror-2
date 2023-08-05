# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.js
    JS interpreter
    Last changed on 2010-05-16 12:15:09+11:00 rev. 184:f0b05c264948 by Dan Kluev <orion@ssorion.info>

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


JS interpreter
==============
"""

__docformat__ = 'restructuredtext'

from . import interpreter
if interpreter == 'CPython':
    from .cpython import js
elif interpreter == 'Jython':
    from .jython import js
else:
    from .pure import js

import types
ldict = locals()
for k in js.__dict__:
    v = js.__dict__[k]
    if not k.startswith('__') or not k.endswith('__'):
        ldict[k] = v
