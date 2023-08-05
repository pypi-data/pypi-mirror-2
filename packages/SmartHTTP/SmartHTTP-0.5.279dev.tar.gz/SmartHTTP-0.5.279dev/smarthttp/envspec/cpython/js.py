# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.envspec.cpython.js
    Google V8 JS interpreter
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


Google V8 JS interpreter
========================
"""
__docformat__ = 'restructuredtext'

try:
    import PyV8
    class JSEngine(PyV8.JSContext):
        def eval(self, *args, **kw):
            self.enter()
            return PyV8.JSContext.eval(self, *args, **kw)
    
    JSClass   = PyV8.JSClass
    JSEnabled = True
except Exception:
    JSEnabled = False
    JSClass   = object
    JSEngine  = None
