# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.translators.infoseek
    Client for translation.infoseek.co.jp
    Last changed on 2010-07-26 19:03:56+11:00 rev. 286:5bad0f3a5211 by Dan Kluev <dan@kluev.name>

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


Client for translation.infoseek.co.jp
=====================================
"""
from . import *

class Infoseek(SpecificSite):
    u"""Site handler for Infoseek translator, which provides accurate Ja/En translations.
    
    >>> site = Infoseek()
    >>> word = site.translate(word=u"水")
    >>> word.data.translation
    u'Water'
    
    """
    domain = 'translation.infoseek.co.jp'
    map    = SmartMap([
           ('translate', '/', dict()),
           ])
           
    def __init__(self, *t, **d):
        SpecificSite.__init__(self, *t, **d)
        self.token = None

    def prepare(self):
        resp = self.load('translate')
        self.get_token(resp)

    def get_token(self, resp):
        token_input = resp.assertHTML().assertXPathOne("/html/body/div//input[@name='token']")
        self.token = token_input.get("value")
        
    def translate(self, word=None, from_l='ja', to_l='en'):
        if not self.token:
            self.prepare()
        if type(word) == unicode:
            word_enc = word.encode('utf-8')
        else:
            word_enc = word
        if to_l == 'en' and from_l == 'ja':
            selector = '1'
        else:
            selector = '0'
        data = {'ac':'Text', 'lng':'en', 'original':word_enc, 'selector':selector, 'token':self.token, 'submit':'　翻訳'}
        resp = self.request(self.url('translate'), data=data)
        self.get_token(resp)
        doc = resp.assertHTML()
        converted = doc.assertXPathOne("/html/body/div//textarea[@name='converted']")
        word = converted.text
        if type(word) == str:
            word = unicode(word, 'utf-8')
        self.log.debug("Word: %s, token: %s" % (word, self.token))
        return self.ok(SmartDict(translation=word))
