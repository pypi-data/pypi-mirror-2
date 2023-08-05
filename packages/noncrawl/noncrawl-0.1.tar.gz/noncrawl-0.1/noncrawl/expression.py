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

##[ Name        ]## expression
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls expressions
##[ Start date  ]## 2010 July 30

import re
import fnmatch
import noncrawl.various as various

URL = 1
DOMAIN = 2
AND = 3
OR = 4
EXPRESSION = 5
OPERATOR = 6

class Expression:
    def __init__(self, raw, **kargs):
        self.error = kargs.get('error') or various.usable_error
        raw = raw.strip()
        if not raw or raw.startswith('#'):
            self.delete = True
            return

        spl = raw.split(' ')
        l = len(spl)
        if l < 2:
            self.wrong_syntax(raw, 'missing something')
            return
        noy = spl[0]
        if noy not in 'yn':
            # This is NOT a y|n thing
            noy = 'y'
            spl.insert(0, None)
        self.white = noy == 'y'

        self.exprs = []
        ts = spl[1:]
        while len(ts) > 1:
            typ = ts[0]
            exp = ts[1]
            if typ not in ('url', 'domain'):
                self.wrong_syntax(raw, '"%s" must be "url" or "domain"'
                                  % typ)
                return
            typ = (typ == 'url' and URL) or \
                (typ == 'domain' and DOMAIN)
            try:
                if not exp.startswith('*'):
                    exp = re.compile(exp)
                else:
                    exp = fnmatch.translate(exp[1:])
                    exp = re.compile(exp)
            except Exception, error:
                self.wrong_syntax(raw, repr(error))
                return
            self.exprs.append((EXPRESSION, typ, exp))

            ts = ts[2:]
            if len(ts) > 2:
                # Another series
                o = (ts[0] == '&&' and AND) or (ts[1] == '||' and OR)
                self.exprs.append((OPERATOR, o))
                ts = ts[1:]
            else:
                break
        if len(ts) > 0:
            self.wrong_syntax(raw, 'missing something, but not fatal',
                              False)

        self.temp_container = various.URLContainer()

    def wrong_syntax(self, raw, msg, delete=True):
        self.error('syntax error in expression "%s"; %s'
                          % (raw, msg))
        if delete:
            self.delete = delete
        return

    def match(self, url):
        ok = self.temp_container.new(url)
        if ok:
            return self.is_ok(self.temp_container)
        else:
            # Not a URL
            return False

    def is_ok(self, info):
        status = True
        operator = AND
        for x in self.exprs:
            w = x[0]
            t = x[1]
            if w == EXPRESSION:
                string = (t == URL and info.url) \
                    or (t == DOMAIN and info.domain)
                match = x[2].match(string) is not None
                if operator == AND:
                    status = status and match
                elif operator == OR:
                    status = status or match
            elif w == OPERATOR:
                operator = t

        if self.white:
            return status
        else:
            return not status
