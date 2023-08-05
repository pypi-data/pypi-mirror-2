# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.shimmie
    Client for Shimmie and Shimmie 2 applications
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

http://12ch.ru/macro/index.php
http://www.animemahou.com/tags/list
http://yaranaiko.net/
http://thedoi.net/post/list
http://booru.nanochan.org/tags/popularity
http://angelhq.net/
http://rule34.paheal.net/post/list
http://www.tentaclerape.net/imageboard/index.php
http://dontstickthatthere.com/shimmie/post/list
http://munemune.net/index.php?q=/post/list
http://vgb-portal.com/chan/post/list
http://chan.aniview.eu/post/list
http://gallery.burrowowl.net/
http://www.clubetchi.com/gpx/post/list
>>> site = Shimmie2(url='http://angelhq.net/')
>>> tags = site.get_tags(order='count')
>>> len(tags.data.tags) > 10
True
"""
from smarthttp.sites.galleries import *

class Shimmie2(Gallery):
    proto = 'http'

    def view_tag_url(self, tag, page=1, **kw):
        kw = SmartDict(kw, "")._join({'tag':tag, 'page':page})
        url = u"/post/list/{0.tag}/{0.page}".format(kw)
        return self.compile_url(url)

    def get_tags(self, **kw):
        kw = SmartDict(kw, "")
        url = u'/tags/popularity'
        req = self.request(self.compile_url(url))
        page_res = self.parse_tags(req)
        return self.ok(page_res.data)

    @parser
    def parse_tags(self, req):
        doc = self.assertHTML(req)
        res = SmartDict({'tags':set(), 'pages':0})
        tags = self.assertXPath(doc, '/html/body//div/div/p/a')
        for tag_a in tags:
            tag_s = tag_a.text.rsplit(u'\xa0', 1)
            count = int(tag_s[1].split('(', 1)[1].split(')', 1)[0])
            res.tags.add(Tag(tag=tag_s[0], count=count))
        return self.ok(res)        
