# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.translators.infoseek
    Client for translation.infoseek.co.jp
    Last changed on Wed Apr 14 15:19:03 2010 +1100 rev. 114:7d05f1ad0e97 by Dan Kluev <orion@ssorion.info>

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
"""
from smarthttp.sites.translators import *

class Infoseek(SpecificSite):
    domain = 'translation.infoseek.co.jp'
    def __init__(self, *t, **d):
        SpecificSite.__init__(self, *t, **d)
        self.token = None

    def prepare(self):
        req = self.request('http://translation.infoseek.co.jp/')
        self.get_token(req)

    def get_token(self, req):
        token_input = req.dom.xpath("/html/body/div//input[@name='token']")[0] 
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
        req = self.request('http://translation.infoseek.co.jp/', request="POST", data=data)
        self.get_token(req)
        document = req.dom
        converted = document.xpath("/html/body/div//textarea[@name='converted']")[0]
        word = converted.text
        if type(word) == str:
            word = unicode(word, 'utf-8')
        self.log.info("Word: %s, token: %s" % (word, self.token))
        return self.ok(word)
