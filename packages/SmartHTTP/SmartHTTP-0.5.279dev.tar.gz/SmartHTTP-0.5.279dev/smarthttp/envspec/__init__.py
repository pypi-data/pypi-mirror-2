# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec
    Interpreter-specific code
    Last changed on 2010-05-16 12:45:13+11:00 rev. 185:697a62a32bfb by Dan Kluev <orion@ssorion.info>

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


Interpreter-specific code
=========================

Each implementation should provide:

* :mod:`smarthttp.envspec.http`
* :mod:`smarthttp.envspec.etree`
* :mod:`smarthttp.envspec.js`

Currently package supports following implementations:

* :mod:`smarthttp.envspec.cpython` since 2.5, with `pycurl`, `lxml` and `pyv8` as dependencies.
* :mod:`smarthttp.envspec.jython` since 2.5, with ElementTree
* :mod:`smarthttp.envspec.pure`

"""
__docformat__ = 'restructuredtext'
from ..exceptions import SmartHTTPException
import platform
version = platform.python_version()
if version.startswith('2.6') or version.startswith('3'):
    interpreter = platform.python_implementation()
else:
    if platform.system() == 'Java':
        interpreter = 'Jython'
    else:
        interpreter = 'CPython'

if not interpreter in ['Jython', 'CPython']:
    interpreter = None
