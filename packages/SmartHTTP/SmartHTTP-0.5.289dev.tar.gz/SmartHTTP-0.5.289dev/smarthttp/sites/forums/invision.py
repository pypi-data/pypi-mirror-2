# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.forums.invision
    Invision Power Board site-handler
    Last changed on 2010-05-29 00:41:07+11:00 rev. 249:c664b92c9e32 by Dan Kluev <dan@kluev.name>

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


Invision Power Board site-handler
=================================

.. _smarthttp.sites.forums.invision-InvisionPowerBoard:

:class:`InvisionPowerBoard`
---------------------------


    Scraper for IPB forum
    

.. autoclass:: InvisionPowerBoard
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from . import *

class InvisionPowerBoard(SiteEngine, ForumHandler):
    """
    Scraper for IPB forum
    """
    
    def parse_local_file(self, fp):
        data = open(fp, 'r').read().decode('cp1251')
        res = []
        document = GetDOM(data)
        posts = document.xpath("//div[@class='postcolor']")
        for post in posts:
            exc = post.xpath("./div") + post.xpath("./span[@class='edit']") + post.xpath("./noindex")
            for el in exc:
                post.remove(el)
            text = GetPlainText(post)
            res.append(text)
        return self.result(res)
