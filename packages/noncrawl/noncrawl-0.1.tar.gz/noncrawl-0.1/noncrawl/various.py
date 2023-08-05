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

##[ Name        ]## various
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Various minor (but still important) parts
##[ Start date  ]## 2010 July 27

import sys
from optparse import OptionParser
from threading import Thread

def error(msg, cont=True, pre=None):
    errstr = str(msg) + '\n'
    if pre is not None:
        errstr = pre + ': ' + errstr
    sys.stderr.write(errstr)
    if cont is not True:
        try:
            sys.exit(cont)
        except Exception:
            sys.exit(1)

def usable_error(msg, cont=True):
    error(msg, cont, 'noncrawl: ')

class NewOptionParser(OptionParser):
    def parse_args(self):
        self.options, args = OptionParser.parse_args(self)
        return self.options, args

    def error(self, msg, cont=True):
        opt_exists = 'options' in dir(self)
        if not opt_exists:
            cont = False
        if not opt_exists or self.options.term_verbose:
            error(msg, cont, self.prog + ': error')

class thread(Thread):
    def __init__(self, func, *args):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.setDaemon(True) # self.daemon = True
        self.start()

    def run(self):
        self.func(*self.args)

class ListDict(dict):
    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            self.__setitem__(key, [])
            val = self.get(key)
        return val

class Container:
    pass

class URLContainer(Container):
    url = ''
    domain = ''
    def new(self, url):
        self.url = url
        ss = url.find('//')
        if ss == -1:
            self.url = ''
            self.domain = ''
            return False
        s = url.find('/', ss + 2)
        if s != -1:
            domain = url[:s]
        else:
            domain = url
        domain = domain[ss + 2:]
        self.domain = domain
        return True
