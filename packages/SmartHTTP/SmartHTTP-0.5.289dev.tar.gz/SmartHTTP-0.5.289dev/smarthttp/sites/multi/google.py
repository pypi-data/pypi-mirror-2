# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.multi.google
    Google site-handler
    Last changed on 2010-07-26 19:03:41+11:00 rev. 285:83323a8fc0de by Dan Kluev <dan@kluev.name>

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


Google site-handler
===================

API reference: http://code.google.com/apis/ajax/

.. _smarthttp.sites.multi.google-GoogleAJAX:

:class:`GoogleAJAX`
-------------------

Google AJAX API handler.
    
    >>> site = GoogleAJAX()
    >>> site.parse('language_detect', q="test").data.language
    u'en'
    >>> site.parse('translate', q=u"水", langpair="ja|en").data.translation
    u'Water'
    >>> len(site.parse('search', q="test").data.results) > 0
    True
    
    

.. autoclass:: GoogleAJAX
    :members:
    :undoc-members:

.. _smarthttp.sites.multi.google-Google:

:class:`Google`
---------------



.. autoclass:: Google
    :members:
    :undoc-members:

.. _smarthttp.sites.multi.google-GoogleMaps:

:class:`GoogleMaps`
-------------------



.. autoclass:: GoogleMaps
    :members:
    :undoc-members:

"""

__docformat__ = 'restructuredtext'

from . import *

class Google(SpecificSite):
    domain = u'google.com'

class GoogleMaps(SpecificSite):
    domain = "maps.google.com"
    map = SmartMap([
        ('search', '/m', {'hl':'en', 'q':None, 'start':None, 'sa':None}),
        ('clear_location', '/m', {'hq':True, 'q':None, 'hl':'en', 'action':'setclrloc', 'sig':'AMctaOJiRruYnA_zlv6tqUTHUEq0zawknw'}),
        ])
    parser = map.parser
    
    def search_mobile(self, location, page=None):
        start = None
        if page:
            start = page * 10
        url = self.url('search_mobile', q=location, start=page)
        req = self.request(url)
        return self.parse_search(req)

    @parser
    def parse_search_mobile(self, resp):
        """
        Page has 3 variants:
        1. List of matches
        2. Single match with map
        3. List of suggestions
        """
        doc = resp.assertHTML()
        map_img   = doc.xpath("/html/body/div/div/div/img[@alt='map']")
        mean_span = doc.xpath("/html/body/div/div/span[@class='m']")
        results   = doc.xpath("/html/body/div/div/div", classes='c0')
        location  = doc.xpath("/html/body/div/div[@class='l']/span")
        res = SmartDict(dict(results=[], did_you_mean=False, map_img=False, location=None))

        if location:
            res.location = location[0].plaintext
        self.log.info("Resuls: {0}, DYM: {1}, Map: {2}".format(bool(results), bool(mean_span), bool(map_img)))
        if mean_span and not results:
            self.log.info("This is 'did you mean'")
            res.did_you_mean=True
            div = mean_span[0].getparent()
            for link in self.assertXPath(div, './a'):
                addr = link.href.params['q'][0]
                entry = SmartDict(dict(name='', latitude=0.0, longitude=0.0, cid=0, telephone=0, address=''))
                entry.address = addr
                res.results.append(entry)
                
        elif map_img:
            self.log.info("This is map")
            res.map_img = True
        else:
            for result in results:
                entry = SmartDict(dict(name='', latitude=0.0, longitude=0.0, cid=0, telephone=0, address=''))
                link = self.assertXPathOne(result, './a[1]')
                latlng = self.assertKey(link.href.params, 'latlng')[0]
                a_tel = result.xpath('./a[3]')

                entry.address = unicode(self.assertXPathOne(result, './span').text)
                entry.name = link.plaintext
                if a_tel:
                    entry.telephone = unicode(a_tel[0].href.path)
                entry.latitude, entry.longitude, entry.cid = unicode(latlng).split(',')

                res.results.append(entry)
        return self.ok(res)

    
class GoogleAJAX(SpecificSite):
    u"""Google AJAX API handler.
    
    >>> site = GoogleAJAX()
    >>> site.parse('language_detect', q="test").data.language
    u'en'
    >>> site.parse('translate', q=u"水", langpair="ja|en").data.translation
    u'Water'
    >>> len(site.parse('search', q="test").data.results) > 0
    True
    
    """
    
    domain = "ajax.googleapis.com"
    map = SmartMap([
        ('search',          '/ajax/services/search/web', dict(v='1.0', q="", hl='en')),
        ('maps',            '/ajax/services/search/local', dict(v='1.0', q="")),
        ('language_detect', '/ajax/services/language/detect', dict(v='1.0', q="")),
        ('translate',       '/ajax/services/language/translate', dict(v='1.0', q="", langpair="en|ru")),
        ])
    langs = {
        'af':'Afrikaans', 'sq':'Albanian', 'am':'Amharic', 'ar':'Arabic', 'hy':'Armenian', 'az':'Azerbaijani', 'eu':'Basque',
        'be':'Belarusian','bn':'Bengali','bh':'Bihari','bg':'Bulgarian','my':'Burmese','ca':'Catalan','chr':'Cherokee',
        'zh':'Chinese','zh-CN':'Chinese_simplified','zh-TW':'Chinese_traditional','hr':'Croatian','cs':'Czech','da':'Danish',
        'dv':'Dhivehi','nl':'Dutch','en':'English','eo':'Esperanto','et':'Estonian','tl':'Filipino','fi':'Finnish',
        'fr':'French','gl':'Galician','ka':'Georgian','de':'German','el':'Greek','gn':'Guarani','gu':'Gujarati','iw':'Hebrew',
        'hi':'Hindi','hu':'Hungarian','is':'Icelandic','id':'Indonesian','iu':'Inuktitut','it':'Italian','ja':'Japanese',
        'kn':'Kannada','kk':'Kazakh','km':'Khmer','ko':'Korean','ku':'Kurdish','ky':'Kyrgyz','lo':'Laothian','lv':'Latvian',
        'lt':'Lithuanian','mk':'Macedonian','ms':'Malay','ml':'Malayalam','mt':'Maltese','mr':'Marathi','mn':'Mongolian',
        'ne':'Nepali','no':'Norwegian','or':'Oriya','ps':'Pashto','fa':'Persian','pl':'Polish','pt-PT':'Portuguese',
        'pa':'Punjabi','ro':'Romanian','ru':'Russian','sa':'Sanskrit','sr':'Serbian','sd':'Sindhi','si':'Sinhalese',
        'sk':'Slovak','sl':'Slovenian','es':'Spanish','sw':'Swahili','sv':'Swedish','tg':'Tajik','ta':'Tamil','tl':'Tagalog',
        'te':'Telugu','th':'Thai','bo':'Tibetan','tr':'Turkish','uk':'Ukrainian','ur':'Urdu','uz':'Uzbek','ug':'Uighur','vi':'Vietnamese'
    }

    parser = map.parser

    def search_maps(self, location):
        url = self.url('maps', q=location)
        resp = self.request(url)
        return self.parse_search_maps(resp)
        

    @parser
    def parse_search_maps(self, resp):
        doc = resp.assertJSON()
        data = doc.assertKey('responseData')
        result = data.assertKey('results')
        res = SmartDict(dict(results=[]))
        if result:
            result = SmartDict(result[0])
            entry = SmartDict(dict(name='', latitude=0.0, longitude=0.0, cid=0, telephone=0, address='', city='', country=''))
            entry.latitude = result.lat
            entry.longitude = result.lng
            entry.name = result.titleNoFormatting
            if result.phoneNumbers:
                entry.telephone = result.phoneNumbers[0]['number']
            entry.city = result.city
            entry.country = result.country
            if result.addressLines:
                entry.address = u' '.join(result.addressLines)
            res.results.append(entry)
        return self.ok(res)
    
    @parser('language_detect')
    def parse_language_detect(self, resp):
        doc = resp.assertJSON()
        response = doc.assertKey('responseData')
        language = response.assertKey('language')
        return self.ok(SmartDict(language=language))

    def translate(self, text, from_l='ru', to_l='en'):
        return self.parse_translate(self.load('translate', q=text, langpair="{0}|{1}".format(from_l, to_l)))
    
    @parser('translate')
    def parse_translate(self, resp):
        doc = resp.assertJSON()
        response = doc.assertKey('responseData')
        trans    = response.assertKey('translatedText')
        return self.ok(SmartDict(translation=trans))

    @parser('search')
    def parse_search(self, resp):
        doc = resp.assertJSON()
        response = doc.assertKey('responseData')
        results  = response.assertKey('results')
        return self.ok(SmartDict(results=results))
