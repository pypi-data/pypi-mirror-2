# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.news.lenta
    Lenta.ru site-handler
    Last changed on 2010-05-29 00:41:07+11:00 rev. 249:c664b92c9e32 by Dan Kluev <dan@kluev.name>

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


Lenta.ru site-handler
=====================

Usage:
>>> r = LentaRu().get_news_list()
>>> not r.error and 'russia' in r.data.keys()
True
>>> r = LentaRu().get_news_list('russia')
>>> not r.error and 'russia' in r.data.keys()
True

.. _smarthttp.sites.news.lenta-LentaRu:

:class:`LentaRu`
----------------


    Scraper for lenta.ru news site
    

.. autoclass:: LentaRu
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from . import *

class LentaRu(SpecificSite, NewsSite):
    """
    Scraper for lenta.ru news site
    """
    domain = 'lenta.ru'
    categories = ['russia', 'xussr', 'ukraine', 'world', 'america', 'germany', 'economy', 'finance',\
                  'business', 'netvert', 'crime', 'auto', 'realty', 'most', 'culture', 'kino',\
                  'music', 'sport', 'science', 'internet', 'digital', 'game', 'mil', 'oddly']
    _re_date = re.compile(r"""(\d+)\.(\d+) (\d+)\:(\d+)""")
    def get_news_list(self, category=''):
        """
        Loads main page or category page and returns list of news
        """
        if category and not category in self.categories:
            return self.error(u"Unknown category %s" % category)

        page = self.request("%s/" % category)
        if page.error or page.code != 200:
            return self.error_http(page)
        
        doc  = page.dom
        if not doc:
            return self.error_html(page)
        
        if category:
            return self._parse_category(doc, category)
        else:
            return self._parse_main(doc)

    def _parse_date(self, datestr):
        m   = self._re_date.match(datestr).groups()
        now = datetime.datetime.now()
        return datetime.datetime(year=now.year, month=int(m[1]), day=int(m[0]), hour=int(m[2]), minute=int(m[3]))

    def _parse_category(self, document, category):
        result = {category:[]}
        news_divs = document.xpath('/html/body/table/tr/td[@class="razdel-news"]/div')
        if not news_divs:
            return self.error_parse(xpath='/html/body/table/tr/td[@class="razdel-news"]/div')
        
        for div in news_divs:
            if div.get('class').startswith('news'):
                link = div.xpath('./h2/a') or div.xpath('./h4/a')
                img   = div.xpath('./a/img')
                entry = {'date':self._parse_date(div.xpath('./div[@class="dt"]')[0].text),
                         'img':img and img[0].get('src') or None,
                         'url':link[0].get('href'),
                         'subject':link[0].text,
                         'description':div.xpath('./p')[0].text
                         }
                result[category].append(entry)
        return self.result(result)
    
    def _parse_main(self, document):
        result = {}
        categories = document.xpath('/html/body/table[@class="peredovica"]')
        if not categories:
            return self.error_parse(xpath='/html/body/table[@class="peredovica"]')

        for cat in categories:
            category_a = cat.xpath('.//td[@class="nav"]/a')
            news_td = cat.xpath('.//td[@class="glavnoe2"]//tr[@valign="top"]/td')
            # Omit 'most popular' and 'most important' sections since we scrape all news
            if news_td and category_a: 
                category = filter(bool, category_a[0].get('name').split('/'))[-1].split('.', 1)[0]
                result[category] = []
                for td in news_td:
                    if td.get('class') == 'last':
                        link  = td.xpath('./a')[0]
                        img   = link.xpath('./img')
                        entry = {'date':self._parse_date(td.xpath('./div[@class="dt"]')[0].text),
                                 'url':link.get('href'),
                                 'img':img and img[0].get('src') or None,
                                 'description':td[-1].text,
                                 'subject':td.xpath('./a')[0][-1].text
                                 }
                        result[category].append(entry)
                    elif 'top' in td.get('class'):
                        for div in td.xpath('./div'):
                            img = div.xpath('./a/img')
                            desc = div.xpath('./span[2]')[0]
                            link = desc.xpath('./a')[0]
                            entry = {'date':self._parse_date(div.xpath('./span[@class="dt"]')[0].text),
                                     'url':link.get('href'),
                                     'img':img and img[0].get('src') or None,
                                     'subject':u"%s%s%s" % (desc.text, link.text, link.tail),
                                     'description': u'',
                                     }
                            result[category].append(entry)
        return self.result(result)
                        
            
        
