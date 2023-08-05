# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.danbooru
    Client for Danbooru gallery engine
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
>>> site = Danbooru(url='http://danbooru.donmai.us/')
>>> tags = site.get_tags(order='count')
>>> len(tags.data.tags) == 50
True
"""
from smarthttp.sites.galleries import *

class Danbooru(Gallery):
    def view_tag_url(self, tag):
        url = u"/post/index"
        return self.compile_url(url, {'tags':tag})
    
    def get_tags(self, order='count', **kw):
        kw = SmartDict(kw, "")._join({'order':order})
        url=u"/tag?type={0.type}&commit=Search&name={0.name}&order={0.order}".format(kw)
        req = self.request(self.compile_url(url, {'page':kw.page}))
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return self.ok(page_res.data)
    
    @parser
    def parse_tags(self, req):
        doc = self.assertHTML(req)
        tbody = self.assertXPathOne(doc, "/html/body/div[@id='content']/table/tbody")
        tags  = tbody.xpath('./tr')
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        for tag_tr in tags:
            tds = self.assertXPath(tag_tr, './td', 3)
            count = int(tds[0].text)
            name  = tds[1][-1].text
            types = map(lambda x:x.strip(), tds[2].text.split('(')[0].split(','))
            if name:
                res.tags.add(Tag(name, count, types))
        paginator = self.assertXPathOne(doc, "/html/body/div[@id='content']/div/div[@class='pagination']")
        curr = self.assertXPathOne(paginator, "./span[@class='current']")
        pages = self.assertXPath(paginator, './a')
        res.page = int(curr.text)
        res.pages = int(pages[-2].text)
        return self.ok(res)

