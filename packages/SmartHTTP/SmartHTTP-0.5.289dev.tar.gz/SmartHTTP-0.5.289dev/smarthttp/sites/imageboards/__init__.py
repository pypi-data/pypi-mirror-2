# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.imageboards
    Imageboards site-handlers
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


Imageboards site-handlers
=========================

:mod:`wakaba`
:mod:`hanabira`
:mod:`kusaba`
:mod:`kareha`
:mod:`orphereus`
:mod:`nullchan`

.. _smarthttp.sites.imageboards-Thread:

:class:`Thread`
---------------



.. autoclass:: Thread
    :members:
    :undoc-members:

.. _smarthttp.sites.imageboards-Board:

:class:`Board`
--------------



.. autoclass:: Board
    :members:
    :undoc-members:

.. _smarthttp.sites.imageboards-File:

:class:`File`
-------------



.. autoclass:: File
    :members:
    :undoc-members:

.. _smarthttp.sites.imageboards-Post:

:class:`Post`
-------------



.. autoclass:: Post
    :members:
    :undoc-members:

.. _smarthttp.sites.imageboards-Imageboard:

:class:`Imageboard`
-------------------

Mix-in for Imageboards.

    Subclasses must implement:

       * get_boards()
       * get_board()
       * get_thread()
       * make_post()

    

.. autoclass:: Imageboard
    :members:
    :undoc-members:

.. _smarthttp.sites.imageboards-Event:

:class:`Event`
--------------



.. autoclass:: Event
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from .. import *

class Imageboard(object):
    """Mix-in for Imageboards.

    Subclasses must implement:

       * get_boards()
       * get_board()
       * get_thread()
       * make_post()

    """
    def get_boards(self):
        raise NotImplemented(self)

    def get_board(self):
        raise NotImplemented(self)

    def get_thread(self):
        raise NotImplemented(self)

    def make_post(self): 
        raise NotImplemented(self)

class Board(object):
    name = None
    site = None
    threads = None
    def __init__(self, name=None, site=None, threads=None, **kw):
        self.name = name
        self.site = site
        self.threads = set()
        if threads:
            for tdict in threads:
                thread = Thread(board=self, **strdict(tdict))
                self.threads.add(thread)

    def __repr__(self):
        return u"<Board('{0.url}')>".format(self.site.url('board', board=self.name, page='index'))

class Thread(object):
    board = None
    display_id = 0
    posts = None
    title = u''
    archived = False
    invisible = False

    def __init__(self, board, display_id=0, posts=None, title=u'', archived=False, invisible=False, **kw):
        self.board = board
        self.display_id = int(display_id)
        self.title = title
        self.archived = archived
        self.invisible = invisible
        self.posts = set()
        if posts:
            for pdict in posts:
                post = Post(thread=self, **strdict(pdict))
                self.posts.add(post)

    def __repr__(self):
        return u"<Thread(/{0.board.name}/{0.display_id})>".format(self)

class Post(object):
    thread = None
    display_id = 0
    post_id    = 0
    date  = None
    message = u""
    subject = u""
    files = None
    name  = u""
    sage  = False
    invisible = False
    inv_reason = u""
    op    = False
    def __init__(self, thread, display_id, post_id, date, message, subject, files, name, sage, op, invisible=False, inv_reason=u"", **kw):
        self.thread = thread
        self.display_id = int(display_id)
        self.post_id = int(post_id)
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.message = message
        self.subject = subject
        self.name = name
        self.sage = sage
        self.invisible = invisible or (self.op and thread.invisible)
        self.inv_reason = inv_reason
        self.op = op
        self.files = set()
        for fdict in files:
            f = File(post=self, **strdict(fdict))
            self.files.add(f)

    @property
    def get_admin_url(self):
        return self.thread.board.site.url('post_admin', post_id=self.post_id)

    @property
    def get_url(self):
        return self.thread.board.site.url('thread_post', board=self.thread.board.name, thread_id=self.thread.display_id, post_id=self.display_id)
    
class File(object):
    post = None
    rating = u"unrated"
    filename = u""
    src = u""
    thumb = u""
    file_id = 0
    ftype = u"image"
    size = 0
    def __init__(self, post, rating, src, thumb, file_id, type, size, filename=u"", **kw):
        self.post = post
        self.rating = rating
        self.filename = filename
        self.size = size
        self.file_id = int(file_id)
        self.thumb = thumb
        self.src = src
        self.ftype = type

    @property
    def get_url(self):
        """
        .. todo:: Temp hack till URL() is finished

        """
        if not '://' in self.src:
            return u"http://{0.domain}/{1.src}".format(self.post.thread.board.site, self)
        else:
            return self.src

class Event(object):
    date = None
    event = None
    def __init__(self, date=None, event=None, **kw):
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.event = event
