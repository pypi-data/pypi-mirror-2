# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.jvwall
    JVWall site-handler
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


JVWall site-handler
===================

>>> site = JVWall()
>>> tags = site.get_tags()
>>> len(tags.data.tags) > 10
True

.. _smarthttp.sites.galleries.jvwall-JVWall:

:class:`JVWall`
---------------



.. autoclass:: JVWall
    :members:
    :undoc-members:

"""
from . import *

class JVWall(SpecificSite, Gallery):
    domain = 'mjv-art.org'
    base_path = '/jvwall'
    proto  = 'http'
    map = SmartMap([ 
        ('tags', '/view_all_tags/:page', dict(page=0, lang='ru', sort_by_num=1, search_text='')),
        ('tag', '/view_posts/:page', dict(page=0, search_tag='', lang='ru')),
        ('image', '', dict()),
        ])
    parser = map.parser

    def get_tags(self, page=0):
        req = self.load('tags', page=page)
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return page_res
        
    @parser
    def parse_tags(self, req):
        doc = req.assertHTML()
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        tags_el = doc.assertXPath("/html/body/div[@id='page']/div[@id='content']/ul/li")
        for tag_el in tags_el:
            links = tag_el.assertXPath('./a', 3)
            tag = unicode(links[0].text).strip()
            tag_ru = unicode(links[1].text).strip()
            tag_jp = unicode(links[2].text).strip()
            count = int(links[2].tail.rsplit('(', 1)[1].split(')', 1)[0])
            res.tags.add(Tag(tag, count, [], name_ru=tag_ru, name_jp=tag_jp))
        return self.ok(res)
        
        
