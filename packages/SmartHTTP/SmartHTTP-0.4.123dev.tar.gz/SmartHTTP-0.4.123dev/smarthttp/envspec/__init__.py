# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec
    This module determines interpreter version and loads appropriate interpreter-specific modules
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
import platform
version = platform.python_version()
if version.startswith('2.6') or version.startswith('3'):
    interpreter = platform.python_implementation()
else:
    if platform.system() == 'Java':
        interpreter = 'Jython'
    else:
        interpreter = 'CPython'

if interpreter == 'CPython':
    from .cpython import http
elif interpreter == 'Jython':
    from .jython import http
else:
    raise Exception('Unsupported interpretator: %s (%s)' % (interpretator, version))
