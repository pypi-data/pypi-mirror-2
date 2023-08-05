# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.gelbooru
    Client for Gelbooru gallery
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
>>> site = Gelbooru()
>>> tags = site.get_tags(order='index_count')
>>> len(tags.data.tags) > 10
True
"""
from smarthttp.sites.galleries import *

class Gelbooru(SpecificSite):
    domain = 'gelbooru.com'
    proto = 'http'

    def view_tag_url(self, tag):
        url = u"/index.php"
        return self.compile_url(url, {'page':'post', 's':'list', 'tags':tag})

    def get_tags(self, page=0, name='all', sort='desc', order='index_count', **kw):
        """
        http://gelbooru.com/index.php?page=tags&s=list&tags=all&sort=desc&order_by=index_count
        """
        kw = SmartDict(kw, "")._join({'name':name, 'sort':sort, 'order':order})
        kw.pid = page * 50
        url=u"index.php?page=tags&s=list&tags={0.name}&sort={0.sort}&order_by={0.order}&pid={0.pid}".format(kw)
        req = self.request(self.compile_url(url))
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        
        res.tags = page_res.data
        
        return self.ok(res)

    @parser
    def parse_tags(self, req):
        doc = self.assertHTML(req)
        rows = doc.xpath("/html/body/div[@id='content']/table/tr")
        if len(rows) > 1:
            rows.pop(0)
            tags = []
            for row in rows:
                count = int(row[0].text)
                tag   = row[1][0][0].text
                types = map(lambda x:x.strip(), row[2].text.split('(')[0].split(','))
                if tag:
                    tags.append(Tag(tag, count, types))
            return self.ok(tags)
        else:
            return self.error('Nothing found')

