# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.client.platforms
    Platform imitation classes
    Last changed on 2010-05-15 00:11:48+11:00 rev. 165:5f0a0a2255cc by Dan Kluev <orion@ssorion.info>

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
import random

class Hardware:
    pass

class OperatingSystem:
    hardware = None
    def __init__(self):
        self.hardware = Hardware()

    def string(self):
        return u""

class Linux(OperatingSystem):
    version_str = 'Linux'
    ui       = 'X11'
    def string(self):
        return "X11; U; Linux i686"

class Windows(OperatingSystem):
    version = None
    versions = ['5.0', '5.1', '5.2', '6.0', '6.1']
    ui      = 'Windows'
    def __init__(self):
        OperatingSystem.__init__(self)
        self.version = random.choice(self.versions)
        self.version_str = "Windows NT {0}".format(self.version)

    def string(self):
        return "Windows; U; Windows NT {0.version}".format(self)

class MacOSX(OperatingSystem):
    version = None
    versions = ['10.4', '10.5', '10_4_11', '10_5_5', '10_5_6', '10_6']
    ui = 'Macintosh'
    def __init__(self):
        OperatingSystem.__init__(self)
        self.version = random.choice(self.versions)
        self.version_str = "Intel Mac OS X {0}".format(self.version)

all_platforms = [Linux, Windows, MacOSX]
actual_platform = Linux
