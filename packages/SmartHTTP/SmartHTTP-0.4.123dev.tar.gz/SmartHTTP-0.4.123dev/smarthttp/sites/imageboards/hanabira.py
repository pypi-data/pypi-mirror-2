# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.imageboards.hanabira
    Client for Hanabira imageboard engine
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

API reference: hanabira.ru

>>> hanabira = Hanabira(domain='dobrochan.ru')
>>> events = hanabira.get_new_events(count=10)
>>> len(events.data.boards) > 0
True
"""
from smarthttp.sites.imageboards import *

class Hanabira(Imageboard):
    key = None
    def __init__(self, key=None, **kw):
        SiteEngine.__init__(self, **kw)
        self.key = key

    def get_post_url(self, post, thread, board):
        return self.compile_url("/%s/res/%s.xhtml#i%s" % (board, thread, post))

    def get_post_admin_url(self, post_id):
        return self.compile_url("/admin/get_post/%s" % (post_id))


    def get_new_events(self, count=100, since=None):
        url = '/index.js'
        if since:
            since = str(since)
        req = self.request(self.compile_url(url, {'count':count, 'since':since, 'key':self.key}))
        page_res = self.parse_new_events(req)
        return self.ok(page_res.data)
        
    @parser
    def parse_new_events(self, req):
        doc = self.assertJSON(req)
        res = SmartDict({'boards':set(), 'events':set()})
        for bname in doc['boards']:
            bdict = SmartDict({'site':self, 'name':bname, 'threads':doc['boards'][bname]['threads']})._join(doc['boards'][bname]['capabilities'])
            board = Board(**bdict._dict)
            res.boards.add(board)
            
        for evdict in doc['events']:
            event = Event(**strdict(evdict))
            res.events.add(event)
        return self.ok(res)
        
    def get_new_posts(self, post_id=0, count=10):
        url = "/api/chan/posts/%s/%s" % (post_id, count)
        if self.key:
            url = "%s/%s" % (url, self.key)

        posts = self.assertJSON(req)
        return self.result(posts)
    
    def hide_post(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for hide posts")
        url = '/api/admin/post/hide/%s/%s' % (post_id, self.key)
        req = self.request(url)
        doc = self.assertJSON(req)
        return self.result(doc)
        
    def show_post(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for show posts")
        url = '/api/admin/post/show/%s/%s' % (post_id, self.key)
        req = self.request(url)
        doc = self.assertJSON(req)
        return self.result(doc)
    
    def ban_user(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for ban user")
        url = '/api/admin/user/ban/%s/%s' % (post_id, self.key)
        req = self.request(url)
        doc = self.assertJSON(req)
        return self.result(doc)
    
    def unban_user(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for unban user")
        url = '/api/admin/user/unban/%s/%s' % (post_id, self.key)
        req = self.request(url)
        doc = self.assertJSON(req)
        return self.result(doc)

    # Should be fixed later
    def parse_local_file(self, fp):
        data = open(fp, 'r').read().decode('utf-8')
        res = []
        document = GetDOM(data)
        posts = document.xpath('/html/body/div')
        for post in posts:
            text = GetPlainText(post)
            res.append(text)
        return self.result(res)        
