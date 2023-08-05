# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.jvwall
    Client for http://mjv-art.org/jvwall/ gallery
    Last changed on Wed Apr 14 16:47:36 2010 +1100 rev. 119:65729c4a50da by Dan Kluev <orion@ssorion.info>

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
>>> site = JVWall()
>>> tags = site.get_tags()
>>> len(tags.data.tags) > 10
True
"""
from smarthttp.sites.galleries import *

class JVWall(SpecificSite):
    domain = 'mjv-art.org'
    base_path = '/jvwall'
    proto  = 'http'
            
    def view_tag_url(self, tag):
        url = u"view_posts/0"
        return self.compile_url(url, {'search_tag':tag, 'lang':'ru'})

    def get_tags(self, page=0):
        params = SmartDict({'page':page})
        url = u"view_all_tags/{0.page}".format(params)
        req = self.request(self.compile_url(url, {'page':page, 'lang':'ru', 'sort_by_num':'1', 'search_text':''}))
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return self.ok(page_res.data)
        
    @parser
    def parse_tags(self, req):
        doc = self.assertHTML(req)
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        tags_el = self.assertXPath(doc, "/html/body/div[@id='page']/div[@id='content']/ul/li")
        for tag_el in tags_el:
            links = self.assertXPath(tag_el, './a', 3)
            tag = unicode(links[0].text).strip()
            tag_ru = unicode(links[1].text).strip()
            tag_jp = unicode(links[2].text).strip()
            count = int(links[2].tail.rsplit('(', 1)[1].split(')', 1)[0])
            res.tags.add(Tag(tag, count, [], name_ru = tag_ru, name_jp = tag_jp))
        return self.ok(res)
        
        
