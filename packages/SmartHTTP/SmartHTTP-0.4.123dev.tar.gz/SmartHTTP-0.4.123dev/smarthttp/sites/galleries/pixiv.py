# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.pixiv
    Client for Pixiv gallery
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
>>> site = Pixiv()
"""
from smarthttp.sites.galleries import *

class Pixiv(SpecificSite):
    domain = 'www.pixiv.net'
    proto  = 'http'

    def login(self, username, password):
        data = {'mode':'login', 'pass':password, 'pixiv_id':username}
        req = self.request('index.php', data=data)
        if 'location' in req.headers and 'mypage' in req.headers['location']:
            mp = self.request('mypage.php')
            return self.ok(True)
        else:
            return self.error("Could not login")
            
    def view_tag_url(self, tag):
        url = u"/tags.php"
        return self.compile_url(url, {'tag':tag})

    def get_tags(self, page=0, r18=False):
        """
        Get list of tags with image quantity
        >>> site = Pixiv()
        >>> tags = site.get_tags()
        >>> len(tags.data.tags) > 10
        True
        """
        if r18:
            url = u"tags_r18.php"
        else:
            url = u"tags.php"
        req = self.request(self.compile_url(url, {'p':page+1}))
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return self.ok(page_res.data)
        
    @parser
    def parse_tags(self, req):
        doc = self.assertHTML(req)
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        tags_el = self.assertXPath(doc, "/html/body//div[@id='popular_tag']/span")
        for tag_el in tags_el:
            tag = unicode(tag_el[0].text).strip()
            count = int(tag_el[0][0].text)
            res.tags.add(Tag(tag, count, []))
        return self.ok(res)
        
        
