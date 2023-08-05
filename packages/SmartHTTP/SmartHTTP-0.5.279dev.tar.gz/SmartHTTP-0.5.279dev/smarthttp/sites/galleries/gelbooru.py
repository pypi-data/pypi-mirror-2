# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.gelbooru
    Gelbooru site-handler
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


Gelbooru site-handler
=====================

>>> site = Gelbooru()
>>> tags = site.get_tags(order='index_count')
>>> len(tags.data.tags) > 10
True

.. _smarthttp.sites.galleries.gelbooru-Gelbooru:

:class:`Gelbooru`
-----------------



.. autoclass:: Gelbooru
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from . import *

class Gelbooru(SpecificSite, Gallery):
    domain = 'gelbooru.com'
    proto = 'http'
    map = SmartMap([
        ('tags', '/index.php', dict(page='tags', s='list', tags='all', sort='desc', order_by='index_count', pid=0)),
        ('tag',  '/index.php', dict(page='post', s='list', tags='')),
        ])
    parser = map.parser

    def get_tags(self, page=0, **kw):
        """
        http://gelbooru.com/index.php?page=tags&s=list&tags=all&sort=desc&order_by=index_count
        """
        kw = SmartDict(kw, "")
        req = self.load('tags', kw, pid=page*50)
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)        
        return page_res

    @parser
    def parse_tags(self, req):
        doc = req.assertHTML()
        rows = doc.xpath("/html/body/div[@id='content']/table/tr")
        res = SmartDict({'tags':set(), 'pages':0})            
        if len(rows) > 1:
            rows.pop(0)
            for row in rows:
                count = int(row[0].text)
                tag   = row[1][0][0].text
                types = map(lambda x:x.strip(), row[2].text.split('(')[0].split(','))
                if tag:
                    res.tags.add(Tag(tag, count, types))
            return self.ok(res)
        else:
            return self.error('Nothing found')

