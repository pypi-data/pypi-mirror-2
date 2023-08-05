# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.wiki.mediawiki
    Client for MediaWiki applications
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

API reference: http://www.mediawiki.org/wiki/API

>>> site = MediaWiki(url='http://en.wikipedia.org/w/')
>>> len(site.get_list().data.pages) > 10
True
>>> len(site.get_list(ns='template').data.pages) > 10
True
>>> bool(site.get_page(title='Main Page').data.pages.pop().content)
True
"""
from BeautifulSoup import BeautifulStoneSoup
from smarthttp.sites.wiki import *

class MediaWikiTemplate(object):
    parent = None
    name   = None
    content = None
    lines  = None
    count_open = 1
    def __init__(self, parent=None, name=None, content=None, lines=None, line=None):
        self.parent = parent
        if name:
            self.name = name.split('|', 1)[0].split('}}', 1)[0].lower()
        self.content = content
        if not lines:
            lines = []
        self.lines = lines
        if line:
            self.lines.append(line)
            self.name = line.split('|', 1)[0].split('}}', 1)[0].lower()

    def add_line(self, line):
        self.count_open += line.count('{{') - line.count('}}')
        if self.count_open == 0:
            line = line.rsplit('}}', 1)[0]
        self.lines.append(line.strip())

    def walk_line(self, line):
        cl = []
        rest = []
        # find where current template ends, and return rest of list
        for i in range(len(line)):
            if i:
                self.count_open += 1
            self.count_open -= line[i].count('}}')
            if self.count_open <= 0:
                cl.append(line[i].rsplit('}}', self.count_open*-1 + 1)[0])
                self.count_open = 0
                rest = line[i+1:]
                break
            cl.append(line[i])            
        self.lines.append(u'{{'.join(cl).strip())
        return rest
    def get_param(self, idx):
        if self.content:
            params = self.content.split('|')
            if len(params) > idx:
                param = params[idx].strip()
                return param
        return None

    def get_wikilinks(self):
        return self.parent.get_wikilinks(content=self.content)

    def __repr__(self):
        return "<Template {{%s}} at %s>" % (self.name, self.parent)

class MediaWikiPageSection(object):
    page = None
    section = None
    level   = None
    content = None
    header  = None
    sections= None
    def __init__(self, page, section, level, content):
        self.page = page
        self.level = level
        self.section = section
        self.content = content

    def get_sections(self):
        if not self.sections:
            self.header, self.sections = self.page.parse_sections(self.content, level+1)
        return self.sections

    def get_templates(self, content=None):
        return self.page.get_templates(content=self.content, parent=self)

    def get_wikilinks(self, content=None):
        if content is None:
            content = self.content
        return self.page.get_wikilinks(content=content)

    def __repr__(self):
        return "<MediaWikiPageSection(%s, %s)>" % (self.section.encode('utf-8'), self.page.title.encode('utf-8'))
        
class MediaWikiPage(object):
    mediawiki = None
    title = None
    page_id = None
    revision_id = None
    last_edit = None
    ns       = None
    content  = None
    sections = None
    header   = None
    aliases  = None
    re_header = re.compile("""^=(=+)([^=]+)=(=+)$""")
    def __init__(self, mw=None, page_id=None, ns=None, title=None, content=None, aliases=None, revision_id=None, last_edit=None):
        self.mediawiki = mw
        self.page_id = page_id
        self.ns      = ns
        self.title   = title
        self.content = content
        if aliases is None:
            self.aliases = set()
        else:
            self.aliases = aliases
        self.revision_id = revision_id
        if self.revision_id and type(self.revision_id) != int:
            self.revision_id = int(self.revision_id)
        self.last_edit = last_edit
        if self.last_edit and type(self.last_edit) != datetime:
            self.last_edit = datetime.strptime(self.last_edit, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def escaped_title(self):
        return MediaWiki.escaped_title(self.title)

    @property
    def safe_title(self):
        return MediaWiki.safe_title(self.title)

    def load(self):
        data = self.mediawiki.get_page(pages=self)
        if str(self.page_id) in data.data:
            pd = data.data[str(self.page_id)]
            self.content = pd['content']

    def save_to_file(self, path=None, basepath=None):
        if not path and basepath:
            path = u"%s/%s" % (basepath, self.safe_title)
        out = open(path, 'w')
        out.write(u"{0.page_id}|{0.ns}|{0.title}|{0.revision_id}|{1}\n{0.content}".format(self, self.last_edit.strftime("%Y-%m-%dT%H:%M:%SZ")).encode('utf-8'))
        out.close()

    @classmethod
    def load_from_file(cls, path):
        data = open(path, 'r').read().decode('utf-8').split('\n', 1)
        params = data[0].split('|', 5)
        return cls(page_id=int(params[0]), ns=params[1], title=params[2], revision_id=params[3], last_edit=params[4], content=data[1])

    def get_sections(self):
        if not self.sections:
            self.header, self.sections = self.parse_sections(self.content, 1)
        return self.sections

    def parse_sections(self, content, level):
        header = []
        current_section = ""
        csl = header
        sections = {}
        lines = map(lambda x:x.strip(), content.split('\n'))
        for l in lines:
            matched = False
            if l:
                m = self.re_header.match(l)
                if m:
                    g = m.groups()
                    if len(g[0]) == len(g[2]) and len(g[0]) == level:
                        current_section = g[1].strip()
                        if not current_section in sections:
                            sections[current_section] = []
                        csl = sections[current_section]
                        matched = True
            if not matched:
                csl.append(l)
        header = u"\n".join(header)
        result = {}
        for section in sections:
            result[section] = MediaWikiPageSection(page=self, section=section, level=level, content=u"\n".join(sections[section]))
        return header, result

    def get_templates(self, content=None, parent=None):
        """
        {{a}}
        {{b|}}
        {{c|d}}
        {{e}}{{f}}
        {{g|h={{j}}}}
        {{k|l={{n}}}}{{m}}
        """
        if content is None:
            content = self.content
        if not parent:
            parent = self
        lines = map(lambda x:x.strip(), content.split('\n'))
        templates = {}
        current = None
        for l in lines:
            if not '<!--' in l:
                if '{{' in l:
                    ls = l.split('{{')
                    if '}}' in l:
                        if current:
                            rest = current.walk_line(ls)
                            if current.count_open == 0:
                                current.content = u'\n'.join(current.lines)
                                current = None
                        else:
                            rest = ls[1:]
                        if rest:
                            while rest:
                                lp = rest[0]
                                current = MediaWikiTemplate(parent=parent, name=lp)
                                templates.setdefault(current.name, [])
                                templates[current.name].append(current)
                                rest = current.walk_line(rest)
                                if current.count_open == 0:
                                    current.content = u'\n'.join(current.lines)
                                    current = None                                
                    elif current:
                        current.add_line(l)
                    else:
                        current = MediaWikiTemplate(parent=parent, line=ls[1])
                        templates.setdefault(current.name, [])
                        templates[current.name].append(current)
                elif current:
                    current.add_line(l)
            elif current:
                current.add_line(l)
            if current and current.count_open == 0:
                current.content = u'\n'.join(current.lines)
                current = None
        return templates
                
    # [[Link|Repr]] -> (Link, "|Repr", Repr)
    re_wikilinks = re.compile(r"""\[\[([^\]\|]+)(\|([^\]]*))?\]\]""")
    def get_wikilinks(self, content=None):
        """
        Notice: links may contain : and #!, ex. [[Image:Something]], [[WikiPedia:Something]] [[Article#Section]]
        """
        links = {}
        if content is None:
            content = self.content
        lines = map(lambda x:x.strip(), content.split('\n'))
        for l in lines:
            if l and not '<!--' in l:
                m = self.re_wikilinks.findall(l)
                if m:
                    for match in m:
                        link = match[0]
                        name = match[2]
                        if not name:
                            name = link
                        if '#' in link:
                            link = link.split('#', 1)[0].strip()
                        if link:
                            link = MediaWiki.escaped_title(link)
                            if not link in links:
                                links[link] = []
                            links[link].append((link, name))
        return links

    def __repr__(self):
        return "<MediaWikiPage(%s)>" % (self.title.encode('utf-8'))

class MediaWiki(SiteEngine):
    """
    Client for MediaWiki applications.
    """
    map = SmartMap([
        ('page', '/index.php', {'title':'', 'action':'render'}),
        ('render', '/api.php', {'format':'json', 'action':'parse', 'text':'', 'title':'API', 'pst':None, 'uselang':None, 'page':None, 'prop':None}),
        ('expand', '/api.php', {'format':'json', 'action':'expandtemplates', 'text':'', 'title':'API'}),
        ])
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
        SiteEngine.__init__(self, *args, **kw)
        self.pages_content_limit = 50
        self.pages_list_limit = 500
        
    def get_list(self, ns='', from_='', limit=500):
        if ns:
            if ns in self.namespaces:
                ns = self.namespaces[ns]
            else:
                ns = int(ns)
        url = '/api.php?action=query&list=allpages&format=json&apfilterredir=nonredirects'
        req = self.request(self.compile_url(url, {'aplimit':limit, 'apfrom':from_, 'apnamespace':ns}))
        res = self.parse_list(req)
        return res

    @parser
    def parse_list(self, req):
        doc = self.assertJSON(req)
        query = self.assertKey(doc, 'query')
        res = SmartDict({'next':None, 'pages':set()})
        if 'query-continue' in doc:
            res.next = doc['query-continue']['allpages']['apfrom']
        allpages = self.assertKey(query, 'allpages')
        for pd in allpages:
            page = MediaWikiPage(self, pd['pageid'], pd['ns'], pd['title'])
            res.pages.add(page)
        return self.result(res)

    def get_page(self, title=None, page_id=None, revision=None, pages=None):
        if title and type(title) != list:
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
        base_url = '/api.php?action=query&prop=info|revisions&rvprop=content&format=json&redirects'
        
        while title or page_id:
            if title:
                req = title[:self.pages_content_limit]
                title = title[self.pages_content_limit:]
                url = self.compile_url(base_url,
                                       {'titles':u'|'.join(req)})
            elif page_id:
                req = page_id[:self.pages_content_limit]
                page_id = page_id[self.pages_content_limit:]
                url = self.compile_url(base_url,
                                       {'pageids':u'|'.join(req)})
            req = self.request(url)
            res = self.parse_page(req)
            if res:
                result._merge(res.data)
            else:
                self.log.warn(res.error_text)
        return self.result(result)

    @parser
    def parse_page(self, req):
        doc = self.assertJSON(req)
        query = self.assertKey(doc, 'query')
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
                    pageid = 'pageid' in pd and pd['pageid'] or int(pid)
                    content = 'revisions' in pd and unicode(pd['revisions'][0]['*']) or u''
                    revision_id = 'lastrevid' in pd and pd['lastrevid'] or ''
                    last_edit   = 'touched' in pd and pd['touched'] or datetime.now()
                    page_title   = unicode(pd['title'])
                    page_aliases = result.aliases[page_title]
                    #if page_title in instanced:
                    #    page = instanced[page_title]
                    #    page.content = content
                    #    page.aliases = page.aliases.union(page_aliases)
                    #else:
                    page = MediaWikiPage(self, page_id=pageid, ns=pd['ns'], title=page_title, content=content, aliases=page_aliases, revision_id=revision_id, last_edit=last_edit)
                    result.pages.add(page)
                else:
                    result.missing.add(unicode(query['pages'][pid]['title']))                    
        return self.ok(result)

    def get_recentchanges(self, till_date=None):
        """
        http://www.mediawiki.org/wiki/API:Query_-_Lists#recentchanges_.2F_rc
        """

    def render_page(self, title=None):
        url = self.url('page', title=title)
        req = self.request(url)
        return self.ok(SmartDict({'page':req.data, 'title':title}))

    def render_markup(self, text, title=None):
        url = self.url('render', title=title)
        req = self.request(url, data={'text':text})
        return self.parse_render_markup(req)

    @parser
    def parse_render_markup(self, req):
        doc = self.assertJSON(req)
        parsed = self.assertKey(doc, 'parse')
        res = SmartDict(parsed)
        res.text = res.text['*']
        return self.ok(SmartDict(parsed))

    def edit_page(self, title=None, content=None, page=None):
        """
        http://www.mediawiki.org/wiki/API:Edit_-_Create%26Edit_pages
        /api.php?action=query&format=json&prop=info&intoken=edit&titles=Template:test
        Should probably get valid token first.
        """
        if page:
            title = page.title
            content = page.content
        if not title or not content:
            return self.error(u"Should have title and content")
        url = '/api.php'
        req = self.request(self.compile_url(url), data={'action':'edit', 'format':'json', 'title':title, 'text':content, 'token':"+\\"})
        return self.parse_action_result(req)

    @parser
    def parse_action_result(self, req):
        doc = self.assertJSON(req)
        if 'error' in doc:
            return self.error(doc['error']['info'])
        else:
            return self.ok(SmartDict(doc[doc.keys()[0]]))

    @parser
    def expand_templates(self, text, title=None):
        url = '/api.php'
        req = self.request(self.compile_url(url, {'action':'expandtemplates', 'format':'json', 'title':title}), data={'text':text})
        doc = self.assertJSON(req)
        et  = self.assertKey(doc, 'expandtemplates')
        return self.ok(self.assertKey(et, '*'))

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
