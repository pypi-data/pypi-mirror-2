# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.galleries.pixiv
    Pixiv site-handler
    Last changed on 2010-07-14 21:33:19+11:00 rev. 278:e0881dc9b014 by Dan Kluev <dan@kluev.name>

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


Pixiv site-handler
==================

>>> site = Pixiv()

.. _smarthttp.sites.galleries.pixiv-Pixiv:

:class:`Pixiv`
--------------



.. autoclass:: Pixiv
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from . import *

class Pixiv(SpecificSite, Gallery):
    domain = 'www.pixiv.net'
    proto  = 'http'
    map = SmartMap([
        ('login', '/index.php', dict()),
        ('tags', '/tags.php', dict(p=1)),
        ('tag', '/tags.php', dict(tag='', p=1)),

        ('image', '/member_illust.php', dict(mode='medium', illust_id='')),
        ('image_big', '/member_illust.php', dict(mode='big', illust_id='')),
        ('image_bookmarks_list', '/bookmark_illust_user.php', dict(illust_id='', p=1)),

        ('own_profile', '/mypage.php', dict()),
        ('own_bookmarks_images', '/bookmark.php', dict(rest='show', p=1)),
        ('own_bookmarks_users',  '/bookmark.php', dict(type='user', rest='show', p=1)),
        ('own_watchlist',        '/bookmark_new_illust.php', dict(mode='new', p=1)),

        ('user_profile', '/member.php', dict(id='')),
        ('user_bookmarks_users', '/bookmark.php', dict(type='user', rest='show', p=1, id='')),
        ('user_bookmarks_images', '/bookmark.php', dict(rest='show', p=1, id='')),
        ('user_images',  '/member_illust.php', dict(id='', p=1)),
        ])
    parser = map.parser
    
    def login(self, username, password):
        data = {'mode':'login', 'pass':password, 'pixiv_id':username}
        resp = self.request(self.url('login'), data=data)
        if 'location' in resp.headers and 'mypage' in resp.headers['location']:
            mp = self.load('own_profile')
            return self.ok(True)
        else:
            return self.error("Could not login", resp=resp)
            
    def get_tags(self, page=0, **kw):
        """
        Get list of tags with image quantity
        .. todo:: Find a way to re-implement tags_r18.php.

        >>> site = Pixiv()
        >>> tags = site.get_tags()
        >>> len(tags.data.tags) > 10
        True
        """
        req = self.load('tags', p=page+1)
        res = SmartDict({'tags':set(), 'pages':0})
        page_res = self.parse_tags(req)
        return page_res
        
    @parser
    def parse_tags(self, resp):
        doc = resp.assertHTML()
        res = SmartDict({'tags':set(), 'pages':0, 'page':0})
        tags_el = doc.assertXPath("/html/body//div[@id='popular_tag']/span")
        for tag_el in tags_el:
            tag = unicode(tag_el[0].text).strip()
            count = int(tag_el[0][0].text)
            res.tags.add(Tag(tag, count, []))
        return self.ok(res)

    @parser('own_bookmarks_users')
    def parse_own_bookmarks_users(self, resp):
        doc = resp.assertHTML()
        res = SmartDict(users=set(), pages=0, page=0, total=0)
        form = doc.assertXPathOne("/html/body/div/div/div/form")
        user_divs = form.assertXPath("./div")
        for user_div in user_divs:
            user = User()
            ava_a = user_div.assertXPathOne('./a[1]')
            user.id = ava_a.href.params['id'][0]
            user.avatar  = ava_a.assertXPathOne('./img').get('src')
            user.name    = unicode(user_div.assertXPathOne('./div[1]').text)
            homesite = user_div.xpath_one('./a[2]')
            if not homesite is None:
                user.homesite = homesite.href.query
            res.users.add(user)
        return self.ok(res)
            
        
