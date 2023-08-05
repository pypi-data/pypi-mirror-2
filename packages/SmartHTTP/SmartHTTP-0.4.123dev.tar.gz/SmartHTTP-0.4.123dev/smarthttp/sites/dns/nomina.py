# -*- coding: utf-8 -*-
"""
    SmartHTTP 
    Release 0.4 rev. 123 on 2010-04-14 09:33:33.212723
    Copyright (C) Thu Aug 27 04:01:12 2009 +1100-Wed Apr 14 20:33:28 2010 +1100,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.dns.nomina
    Site handler for nomina.ru
    Last changed on Wed Apr 14 15:59:34 2010 +1100 rev. 116:120bf48f5532 by Dan Kluev <orion@ssorion.info>

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
>>> nomina = Nomina()
>>> res = nomina.search(domain='nomina.ru')
>>> len(res.data) == 1
True
"""
from smarthttp.sites.dns import *

class Nomina(SpecificSite):
    domain = 'www.nomina.ru'
    proto = 'http'
    def search(self, **kw):
        kw = SmartDict(kw, "")
        url = u"/search/search_by_value.php?domain={0.domain}&owner={0.owner}&nserver={0.nserver}&email={0.email}&phone={0.phone}&fax_no={0.fax}&created={0.created}&paid_till=&free_date=&humip={0.ip}&registrar={0.registrar}".format(kw)
        page = 0
        pages = 1
        domains = set()
        while page < pages:
            req = self.request(self.compile_url(url, {'page':page}))
            page_res = self.parse_search(req)
            if page_res:
                pages = page_res.data.pages
                for domain in page_res.data.domains:
                    domains.add(domain)
            else:
                self.log.warn(page_res.error_text)
            page += 1
        return self.ok(domains)
        
    @parser
    def parse_search(self, req):
        self.assertHTML(req)
        td = self.assertXPathOne(req.document, '/html/body/table/tr[4]/td[2]')
        res = SmartDict({'pages':0}, set)
        domains = td.xpath('./table//a')
        pages_p = self.assertXPathOne(td, './/p[4]')
        pages_a = pages_p.xpath('.//a')
        res.pages = len(pages_a) + 1
        for dom in domains:
            res.domains.add(unicode(dom.text).strip())
        return self.ok(res)
        
