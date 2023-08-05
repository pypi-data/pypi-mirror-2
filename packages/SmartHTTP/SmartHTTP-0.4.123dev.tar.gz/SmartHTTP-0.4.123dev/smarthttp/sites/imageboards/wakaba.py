# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.imageboards.wakaba
    Client for Wakaba imageboard engine
    Last changed on Wed Apr 14 15:53:42 2010 +1100 rev. 115:2a18efae2b83 by Dan Kluev <orion@ssorion.info>

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
from smarthttp.sites.imageboards import *

class Wakaba(Imageboard):
    """
    Scraper for wakaba imageboards
    """
    
    def parse_local_file(self, fp):
        data = open(fp, 'r').read().decode('utf-8')
        res = []
        document = GetDOM(data)
        op = document.xpath('//div/blockquote')
        if not op:
            op = document.xpath('//form/blockquote')
        posts = document.xpath('//td/blockquote')
        for post in op + posts:
            text = GetPlainText(post)
            res.append(text)
        return self.result(res)
