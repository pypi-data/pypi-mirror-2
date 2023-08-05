# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.shimmie
    Shimmie site-handlers
    Last changed on 2010-07-13 18:05:30+11:00 rev. 269:3b1da799f2b6 by Dan Kluev <dan@kluev.name>

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


Shimmie site-handlers
=====================

Site examples
*************

* http://12ch.ru/macro/index.php
* http://www.animemahou.com/tags/list
* http://yaranaiko.net/
* http://thedoi.net/post/list
* http://booru.nanochan.org/tags/popularity
* http://angelhq.net/
* http://rule34.paheal.net/post/list
* http://www.tentaclerape.net/imageboard/index.php
* http://dontstickthatthere.com/shimmie/post/list
* http://munemune.net/index.php?q=/post/list
* http://vgb-portal.com/chan/post/list
* http://chan.aniview.eu/post/list
* http://gallery.burrowowl.net/
* http://www.clubetchi.com/gpx/post/list

Usage
*****

>>> site = Shimmie2(url='http://angelhq.net/')
>>> tags = site.get_tags(order='count')
>>> len(tags.data.tags) > 10
True

.. _smarthttp.sites.galleries.shimmie-Shimmie2:

:class:`Shimmie2`
-----------------



.. autoclass:: Shimmie2
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from . import *

class Shimmie2(SiteEngine, Gallery):
    proto = 'http'
    map = SmartMap([
        ('tag', '/post/list/:tag/:page', dict(page=1)),
        ('tags', '/tags/popularity', dict()),
        ('image', '', dict()),
        ])
    
    parser = map.parser
    
    def get_tags(self, **kw):
        req = self.load('tags')
        page_res = self.parse_tags(req)
        return page_res

    @parser
    def parse_tags(self, req):
        doc = req.assertHTML()
        res = SmartDict({'tags':set(), 'pages':0})
        tags = doc.assertXPath('/html/body//div/div/p/a')
        for tag_a in tags:
            tag_s = tag_a.text.rsplit(u'\xa0', 1)
            count = int(tag_s[1].split('(', 1)[1].split(')', 1)[0])
            res.tags.add(Tag(tag=tag_s[0], count=count))
        return self.ok(res)        
