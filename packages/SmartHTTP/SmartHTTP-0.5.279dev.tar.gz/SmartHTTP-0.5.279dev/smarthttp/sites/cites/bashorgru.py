# -*- coding: utf-8 -*-
"""
..
    SmartHTTP 
    Release 0.5 rev. 279 on 2010-07-20 04:32:27.374371
    Copyright (C) 2009-2010,
    Authors: Dan Kluev <dan@kluev.name>

    Module smarthttp.sites.cites.bashorgru
    Bash.Org.Ru site-handler
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


Bash.Org.Ru site-handler
========================

.. _smarthttp.sites.cites.bashorgru-BashOrgRu:

:class:`BashOrgRu`
------------------


    Scraper for bash.org.ru
    

.. autoclass:: BashOrgRu
    :members:
    :undoc-members:

"""
__docformat__ = 'restructuredtext'

from . import *

class BashOrgRu(SpecificSite):
    """
    Scraper for bash.org.ru
    """
    domain = 'bash.org.ru'
    
    def parse_local_file(self, fp):
        data = open(fp, 'r').read()
        res = []
        document = GetDOM(data)
        cites = document.xpath("//div[@class='q']/div[2]")
        for cite in cites:
            text = ForcedEncoding(GetPlainText(cite), 'cp1251')
            res.append(text)
        return self.result(res)
