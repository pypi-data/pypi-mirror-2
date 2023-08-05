#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noncrawl: a web crawler creating link soups
# Copyright (C) 2010  Niels Serup

# This file is part of noncrawl.
#
# noncrawl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# noncrawl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with noncrawl.  If not, see <http://www.gnu.org/licenses/>.

##[ Name        ]## whiteblacklist
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls whitelists and blacklists
##[ Start date  ]## 2010 July 30

import noncrawl.various as various
from noncrawl.expression import Expression

base_list = '''
### Search engines ###
# Considering that the result pages of search results naturally change
# frequently, it is not a good idea to allow the dynamic parts of the
# following sites.

n domain **scroogle.org && url .+?\?.*?q=.*
n domain .*?google\.(?!org) && url .+?\?.*?q=.*
n domain **search.yahoo.com && url .+?\?.*?p=.*
n domain **bing.com && url .+?\?.*?q=.*
n domain **altavista.com && url .+?\?.*?q=.*
n domain **ask.com && url .+?\?.*?q=.*
n domain **baidu.com && url .+?\?.*?wd=.*
n domain **sogou.com && url .+?\?.*?query=.*
n domain **duckduckgo.com && url .+?\?.*?q=.*
n domain **cuil.com && url .+?\?.*?q=.*
n domain **yandex.ru && url .+?\?.*?text=.*
n domain **yandex.com && url .+?\?.*?text=.*
n domain **yebol.com && url .+?\?.*?key=.*
'''

class List:
    def __init__(self, system, **kargs):
        self.system = system
        filename = kargs.get('file')
        string = kargs.get('data')
        self.ignore_base = kargs.get('ignore_base')
        if string is not None:
            self.create_from_string(string)
        elif filename is not None:
            self.create_from_file(filename)
        else:
            self.create_basic()

        self.temp_container = various.URLContainer()

    def create_from_file(self, filename):
        fc = open(filename, 'U').read()
        self.create_from_string(fc)

    def create_basic(self):
        self.create_from_string('')

    def create_from_string(self, s):
        if not self.ignore_base:
            s = base_list + '\n' + s
        l = s.split('\n')
        self.white_exprs = []
        self.black_exprs = []
        for x in l:
            e = Expression(x, error=self.system.error)
            if 'delete' not in dir(e):
                if e.white:
                    self.white_exprs.append(e)
                else:
                    self.black_exprs.append(e)

    def is_ok(self, url):
        ok = self.temp_container.new(url)
        if not ok: return False

        for x in self.white_exprs:
            if x.is_ok(self.temp_container):
                return True
        # Else
        for x in self.black_exprs:
            if not x.is_ok(self.temp_container):
                return False
        # Else
        return True
