# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.imageboards.hanabira
    Hanabira site-handler
    Last changed on 2010-07-20 15:31:20+11:00 rev. 279:0e18c726f36b by Dan Kluev <dan@kluev.name>

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


Hanabira site-handler
=====================

API reference: hanabira.ru

>>> hanabira = Hanabira(domain='dobrochan.ru')
>>> events = hanabira.get_new_events(count=10)
>>> len(events.data.boards) > 0
True

.. _smarthttp.sites.imageboards.hanabira-Hanabira:

:class:`Hanabira`
-----------------



.. autoclass:: Hanabira
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from . import *

class Hanabira(SiteEngine, Imageboard):
    map = SmartMap([
        # Generic IB
        ('board',       '/{board}/{page}.xhtml', dict(page=0)),
        ('thread',      '/{board}/res/{thread_id}.xhtml', dict()),
        ('thread_post', '/{board}/res/{thread_id}.xhtml#i{post_id}', dict()),
        ('captcha',     '/captcha/{board}/{rand}.png',         dict(rand=0)),
        ('post',        '/{board}/post/{post_id}{.format}',    dict(post_id='new', format='xhtml')),
        ('delete',      '/{board}/delete{.format}',            dict()),
        
        # Hanabira-specific
        ('events',      '/index.js', dict(count=100, since='', key='')),
        ('post_admin',  '/admin/get_post/{post_id}', dict()),
        ('hide_post',   '/api/admin/post/hide/{post_id}/{key}', dict()),
        ('show_post',   '/api/admin/post/show/{post_id}/{key}', dict()),
        ('ban_user',    '/api/admin/user/ban/{post_id}/{key}', dict()),
        ('unban_user',  '/api/admin/user/unban/{post_id}/{key}', dict()),
        ])
    parser = map.parser

    key = None
    def __init__(self, key=None, **kw):
        SiteEngine.__init__(self, **kw)
        self.key = key

    def get_new_events(self, count=100, since=None):
        if since:
            since = str(since)
        resp = self.load('events', count=count, since=since, key=self.key)
        page_res = self.parse_new_events(resp)
        return self.ok(page_res.data)
        
    @parser('events')
    def parse_new_events(self, resp):
        doc = resp.assertJSON()
        res = SmartDict({'boards':set(), 'events':set()})
        for bname in doc['boards']:
            bdict = SmartDict({'site':self, 'name':bname, 'threads':doc['boards'][bname]['threads']}).update(doc['boards'][bname]['capabilities'])
            board = Board(**bdict)
            res.boards.add(board)
            
        for evdict in doc['events']:
            event = Event(**strdict(evdict))
            res.events.add(event)
        return self.ok(res)
    
    def hide_post(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for hide posts")
        resp = self.load('hide_post', post_id=post_id, key=self.key)
        doc  = resp.assertJSON()
        return self.result(doc)
        
    def show_post(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for show posts")
        resp = self.load('show_post', post_id=post_id, key=self.key)
        doc  = resp.assertJSON()
        return self.result(doc)
    
    def ban_user(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for ban user")
        resp = self.load('ban_user', post_id=post_id, key=self.key)
        doc  = resp.assertJSON()
        return self.result(doc)
    
    def unban_user(self, post_id):
        if not self.key:
            return self.error(u"Admin key is needed for unban user")
        resp = self.load('unban_user', post_id=post_id, key=self.key)
        doc  = resp.assertJSON()
        return self.result(doc)

    @parser('thread')
    def parse_thread(self, resp):
        doc = resp.assertHTML()
        posts = doc.assertXPath('/html/body/div')
        for post in posts:
            text = post.plain_text
            res.append(text)
        return self.ok(res)
