# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.wiki.mediawiki
    MediaWiki site-handler
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


MediaWiki site-handler
======================

API reference: http://www.mediawiki.org/wiki/API

>>> site = MediaWiki(url='http://en.wikipedia.org/w/')
>>> len(site.get_list().data.pages) > 10
True
>>> len(site.get_list(ns='template').data.pages) > 10
True
>>> bool(site.get_page(title='Main Page').data.pages.pop().content)
True

.. _smarthttp.sites.wiki.mediawiki-MediaWiki:

:class:`MediaWiki`
------------------


    Client for MediaWiki applications.
    

.. autoclass:: MediaWiki
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from BeautifulSoup import BeautifulStoneSoup
import urllib
from .markup import MediaWikiTemplate, MediaWikiPageSection, MediaWikiPage
from .. import *

class MediaWiki(SiteEngine, WikiSite):
    """
    Client for MediaWiki applications.
    """
    dateformat = "%Y-%m-%dT%H:%M:%SZ"
    map = SmartMap([
        ('page', '/index.php',      dict(title='', action='render')),
        ('render', '/api.php',      dict(format='json', action='parse', text='', title='API', pst=None, uselang=None, page=None, prop=None)),
        ('rc',     '/api.php',      dict(format='json', action='query', list='recentchanges', rctype='edit|new',\
                                         rcprop='title|timestamp|ids|sizes|flags|user', rclimit=500, rcstart='', rcend='', rcdir='')),
        ('expand', '/api.php',      dict(format='json', action='expandtemplates', text='', title='API')),
        ('edit', '/api.php',        dict(format='json', action='edit', title='', text='', token="+\\")),
        ('allpages', '/api.php',    dict(format='json', action='query', list='allpages', apfilterredir='nonredirects', aplimit=500, apfrom='', apnamespace='')),
        ('query_page', '/api.php',  dict(format='json', action='query', prop='info|revisions|langlinks|images',\
                                         rvprop='ids|timestamp|content', redirects=True, titles='', pageids='')),
        ('query_image', '/api.php', dict(format='json', action='query', prop='info|revisions|imageinfo',\
                                         rvprop='ids|timestamp|content', iiprop='timestamp|url|size', redirects=True, titles='', pageids='')),
        
        ])
    parser = map.parser
    pages_list_limit = 500
    pages_content_limit = 50
    namespaces = {
        'main':0,
        'talk':1,
        'user':2,
        'file':6,
        'media':-2,
        'template':10,
        'category':14
        }
    
    def __init__(self, pages_list_limit=500, pages_content_limit=50, *args, **kw):
        """
        :param pages_list_limit: API limit
        :param pages_content_limit: API limit
        """
        SiteEngine.__init__(self, *args, **kw)
        self.pages_content_limit = pages_content_limit
        self.pages_list_limit = pages_list_limit
        
    def get_list(self, ns='', from_='', limit=500):
        """Get list of pages.
        """
        if ns:
            if ns in self.namespaces:
                ns = self.namespaces[ns]
            else:
                ns = int(ns)
        url = self.url('allpages', aplimit=limit, apfrom=from_, apnamespace=ns)
        req = self.request(url)
        res = self.parse_list(req)
        return res

    @parser
    def parse_list(self, req):
        doc = req.assertJSON()
        query = doc.assertKey('query')
        res = SmartDict({'next':None, 'pages':set()})
        if 'query-continue' in doc:
            res.next = doc['query-continue']['allpages']['apfrom']
        allpages = query.assertKey('allpages')
        for pd in allpages:
            page = MediaWikiPage(self, pd['pageid'], pd['ns'], pd['title'])
            res.pages.add(page)
        return self.result(res)

    def get_page(self, title=None, page_id=None, revision=None, pages=None):
        """
        Retrieve pages specified by params.
        
        .. todo:: clean-up and turn into iterator.
        """
        if title and type(title) != list:
            if type(title) == str or type(title) == unicode:
                title = [title]
            else:
                title = list(title)
        if page_id and type(page_id) != list and type(page_id) != set:
            page_id = [page_id]
        if pages and type(pages) != list:
            pages = [pages]

        instanced = {}
        if pages:
            if not page_id:
                page_id = []
            for page in pages:
                page_id.append(str(page.page_id))
                instanced[page.title] = page
        result = SmartDict({'pages':set(), 'redirects':{}, 'aliases':SmartDict({}, set), 'missing':set()}, set)
        while title or page_id:
            if title:
                req = title[:self.pages_content_limit]
                title = title[self.pages_content_limit:]
                url = self.url('query_page', titles=u'|'.join(req))
            elif page_id:
                req = page_id[:self.pages_content_limit]
                page_id = page_id[self.pages_content_limit:]
                url = self.url('query_page', pageids=u'|'.join(req))
            req = self.request(url)
            res = self.parse_page(req)
            if res:
                result._merge(res.data)
            else:
                self.log.warn(res.error_text)
        return self.result(result)

    @parser
    def parse_page(self, req):
        """
        .. todo:: Should re-use objects for already instanced pages. How?
        """
        doc = req.assertJSON()
        query = doc.assertKey('query')
        result = SmartDict({'pages':set(), 'redirects':{}, 'aliases':SmartDict({}, set), 'missing':set()}, set)
        if 'normalized' in query:
            for redir in query['normalized']:
                result.redirects[redir['from']] = redir['to']
                result.aliases[redir['to']].add(redir['from'])
        if 'redirects' in query:
            for redir in query['redirects']:
                result.redirects[redir['from']] = redir['to']
                result.aliases[redir['to']].add(redir['from'])
        if 'pages' in query:
            for pid in query['pages']:
                if int(pid) > -1:
                    pd = query['pages'][pid]
                    pageid = pd.get('pageid', int(pid))
                    content = 'revisions' in pd and unicode(pd['revisions'][0]['*']) or u''
                    revision_id = pd.get('lastrevid', '')
                    last_edit   = 'touched' in pd and self.date(pd['touched']) or datetime.now()
                    page_title   = unicode(pd['title'])
                    page_aliases = result.aliases[page_title]
                    page = MediaWikiPage(self, page_id=pageid, ns=pd['ns'], title=page_title, content=content, aliases=page_aliases, revision_id=revision_id, last_edit=last_edit)
                    if 'images' in pd:
                        page.images = map(lambda x:x['title'], pd['images'])
                    if 'langlinks' in pd:
                        page.langs = map(lambda x:x['lang'], pd['langlinks'])
                    if 'imageinfo' in pd:
                        page.imageinfo = SmartDict(pd['imageinfo'][0])
                    if 'imagerepository' in pd:
                        page.imagerepository = pd['imagerepository']
                    result.pages.add(page)
                else:
                    result.missing.add(unicode(query['pages'][pid]['title']))                    
        return self.ok(result)

    def get_recentchanges(self, start_date=None, end_date=None, dir=None):
        """Get list of recent changes.

        `API <http://www.mediawiki.org/wiki/API:Query_-_Lists#recentchanges_.2F_rc>`

        Currently limited to end_date, with from-newer-to-older direction
        
        .. todo:: Implement as generator, support all query modes
        
        """
        if not end_date:
            return self.error(u"Not implemented")
        if type(end_date) == str or type(end_date) == unicode:
            end_date = self.date(end_date)
        start_date = None
        last_date  = None
        result = SmartDict(records=set())
        while not last_date or last_date > end_date:
            url = self.url('rc', rcstart=start_date, rcdir='older', rcend=end_date)
            req = self.request(url)
            res = self.parse_recentchanges(req)
            if not res.data.start_date:
                last_date = end_date
            else:
                last_date = res.data.last_date
                start_date = res.data.start_date
            result.records = result.records.union(res.data.records)
        return self.ok(result)

    @parser
    def parse_recentchanges(self, req):
        doc = req.assertJSON()
        query = doc.assertKey('query')
        result = SmartDict(records=set(), last_date=None, start_date=None)
        for record_dict in query['recentchanges']:
            record = SmartDict(record_dict, _hash=record_dict['title'])
            record.timestamp = self.date(record.timestamp)
            result.records.add(record)
            if not result.last_date or record.timestamp < result.last_date:
                result.last_date = record.timestamp
        if 'query-continue' in doc:
            result.start_date = self.date(doc['query-continue']['recentchanges']['rcstart'])
        return self.ok(result)
                
    def render_page(self, title=None):
        req = self.load('page', title=title)
        return self.ok(SmartDict({'page':req.data, 'title':title}))

    def render_markup(self, text, title=None):
        url = self.url('render', title=title)
        req = self.request(url, data={'text':text})
        return self.parse_render_markup(req)

    @parser
    def parse_render_markup(self, req):
        doc = req.assertJSON()
        res = doc.assertKey('parse')
        res.text = res.text['*']
        return self.ok(res)

    def edit_page(self, title=None, content=None, page=None):
        """Edit page content.
        
        `API <http://www.mediawiki.org/wiki/API:Edit_-_Create%26Edit_pages>`
        
        :param title: Title of page to edit.
        :param content: New page content in wiki markup.
        :param page: :class:`~smarthttp.sites.wiki.mediawiki.markup.MediaWikiPage` instance.
        
        .. todo:: Should probably get valid token first.
        """
        if page:
            title = page.title
            content = page.content
        if not title or not content:
            return self.error(u"Should have title and content")
        url = self.url('edit', title=title)
        req = self.request(url, data={'text':content})
        return self.parse_action_result(req)

    @parser
    def parse_action_result(self, req):
        doc = req.assertJSON()
        if 'error' in doc:
            return self.error(doc['error']['info'])
        else:
            return self.ok(SmartDict(doc[doc.keys()[0]]))

    @parser
    def expand_templates(self, text, title=None):
        """
        .. todo:: Remove loading code and rename to parser.
        """
        url = self.url('expand', title=title)
        req = self.request(url, data={'text':text})
        doc = req.assertJSON()
        et  = doc.assertKey('expandtemplates')
        return self.ok(self.assertKey(et, '*'))

    def get_images(self, titles):
        """
        Resolves urls for given list of images and loads them
        """
        images = {}

    @classmethod
    def escaped_title(cls, title):
        # normalize spaces
        title = u' '.join(filter(bool, title.replace('_', ' ').split(' ')))
        # remove weird chars. Basically they should not be there in the first place, but lets be fail-proof
        title = title.replace(u'‎', u'').replace(u'|', u'').replace(u'}', u'').replace(u'{', u'')
        # unquote
        if '%' in title:
            title = urllib.unquote(title.encode('utf-8')).decode('utf-8')
        # unescape html entities
        if '&' in title:
            title = BeautifulStoneSoup(title, convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
        # Capitalize first letter
        title = title[0].upper() + title[1:]
        return title

    @classmethod
    def safe_title(cls, title):
        # Let it be normalized title with spaces and slashes to _
        title = cls.escaped_title(title)
        return title.replace(' ', '_').replace('/', '_')
