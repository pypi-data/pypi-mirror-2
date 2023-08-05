# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.wiki.mediawiki.markup
    MediaWiki markup parsers
    Last changed on 2010-05-26 14:42:13+11:00 rev. 235:20c757895af5 by Dan Kluev <orion@ssorion.info>

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


MediaWiki markup parsers
========================

.. _smarthttp.sites.wiki.mediawiki.markup-MediaWikiPage:

:class:`MediaWikiPage`
----------------------



.. autoclass:: MediaWikiPage
    :members:
    :undoc-members:

.. _smarthttp.sites.wiki.mediawiki.markup-MediaWikiPageSection:

:class:`MediaWikiPageSection`
-----------------------------



.. autoclass:: MediaWikiPageSection
    :members:
    :undoc-members:

.. _smarthttp.sites.wiki.mediawiki.markup-MediaWikiTemplate:

:class:`MediaWikiTemplate`
--------------------------



.. autoclass:: MediaWikiTemplate
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'
import re
from datetime import datetime

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
    images   = None
    imageinfo= None
    imagerepository = None
    langs    = None
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
        return self.mediawiki.escaped_title(self.title)

    @property
    def safe_title(self):
        return self.mediawiki.safe_title(self.title)

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
                            link = self.mediawiki.escaped_title(link)
                            if not link in links:
                                links[link] = []
                            links[link].append((link, name))
        return links

    def __repr__(self):
        return "<MediaWikiPage(%s)>" % (self.title.encode('utf-8'))
