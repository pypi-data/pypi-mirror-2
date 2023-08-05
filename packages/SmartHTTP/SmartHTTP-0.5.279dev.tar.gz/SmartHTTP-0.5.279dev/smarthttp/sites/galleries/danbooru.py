# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.danbooru
    Danbooru site-handler
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


Danbooru site-handler
=====================

>>> site = Danbooru(url='http://danbooru.donmai.us/')
>>> tags = site.get_tags(order='count')
>>> len(tags.data.tags) == 50
True

.. _smarthttp.sites.galleries.danbooru-Danbooru:

:class:`Danbooru`
-----------------



.. autoclass:: Danbooru
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from . import *

class Danbooru(SiteEngine, Gallery):
    map = SmartMap([
        ('tags', '/tag', dict(type='', commit='Search', name='', order='count', page=0)),
        ('tag', '/post/index', dict(tags='')),
        ])
    parser = map.parser

    def get_tags(self, **kw):
        req = self.load('tags', kw)
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return page_res
    
    @parser
    def parse_tags(self, req):
        doc = req.assertHTML()
        tbody = doc.assertXPathOne("/html/body/div[@id='content']/table/tbody")
        tags  = tbody.xpath('./tr')
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        for tag_tr in tags:
            tds = tag_tr.assertXPath('./td', 3)
            count = int(tds[0].text)
            name  = tds[1][-1].text
            types = map(lambda x:x.strip(), tds[2].text.split('(')[0].split(','))
            if name:
                res.tags.add(Tag(name, count, types))
        paginator = doc.assertXPathOne("/html/body/div[@id='content']/div/div[@class='pagination']")
        curr = paginator.assertXPathOne("./span[@class='current']")
        pages = paginator.assertXPath('./a')
        res.page = int(curr.text)
        res.pages = int(pages[-2].text)
        return self.ok(res)

