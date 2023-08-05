#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.lib.httpbot
    Generic bots based on paster scripts.
    Last changed on 2010-04-14 14:50:37+11:00 rev. 111:5efdacc70dde by Dan Kluev <orion@ssorion.info>

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
from smarthttp.lib.simplebot import SimpleBot
from smarthttp.lib.pylonsscript import PylonsScript
import logging
log = None

class HTTPBot(SimpleBot):
    def main():
        pass

# HTTP-bot based on Pylons-script
class PylonsHTTPBot(PylonsScript):
    def main():
        pass
