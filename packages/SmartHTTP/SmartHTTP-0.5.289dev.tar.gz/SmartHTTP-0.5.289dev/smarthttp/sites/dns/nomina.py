# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 289 on 2010-08-19 09:27:31.860316
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.dns.nomina
    nomina.ru site-handler
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


nomina.ru site-handler
======================

>>> nomina = Nomina()
>>> res = nomina.search(domain='nomina.ru')
>>> len(res.data) == 1
True

.. _smarthttp.sites.dns.nomina-Nomina:

:class:`Nomina`
---------------



.. autoclass:: Nomina
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from . import *

class Nomina(SpecificSite):
    domain = 'www.nomina.ru'
    proto = 'http'
    map   = SmartMap([
        ('search', '/search/search_by_value.php',\
         dict(page=0, domain='', owner='', nserver='', email='', phone='',\
              fax_no='', created='', paid_till='', free_date='', humip='', registrar='')),
        
        ])
    parser = map.parser
    
    def search(self, **kw):
        """
        .. todo:: Turn into iterator.
        """
        kw['humip'] = kw.get('ip', '')
        page = 0
        pages = 1
        domains = set()
        while page < pages:
            req = self.load('search', kw, page=page)
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
        doc = req.assertHTML()
        td  = doc.assertXPathOne('/html/body/table/tr[4]/td[2]')
        res = SmartDict({'pages':0}, set)
        domains = td.xpath('./table//a')
        pages_p = td.assertXPathOne('.//p[4]')
        pages_a = pages_p.xpath('.//a')
        res.pages = len(pages_a) + 1
        for dom in domains:
            res.domains.add(unicode(dom.text).strip())
        return self.ok(res)
        
