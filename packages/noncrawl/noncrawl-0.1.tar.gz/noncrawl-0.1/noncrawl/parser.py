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

##[ Name        ]## parser
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Parses data files of projects, extracting useful
                  # data in the process
##[ Start date  ]## 2010 July 31

import os.path
from noncrawl.expression import Expression
import noncrawl.various as various

class Parser:
    def __init__(self, path, **kargs):
        self.path = path
        self.use_aliases = kargs.get('use_aliases') or True
        self.error = kargs.get('error') or various.usable_error

        # Open project files
        try:
            self.links = [l.split('\n') for l in
                          open(os.path.join(path, 'links')
                               ).read().split('\n\n')]
        except Exception:
            self.error('error in links file', False)

        if self.use_aliases:
            try:
                raw_aliases = [l.split('\n') for l in
                               open(os.path.join(path, 'aliases')
                                    ).read().split('\n\n')]
            except Exception:
                self.error('error in aliases file', False)
            aliases = various.ListDict()
            for x in raw_aliases:
                try:
                    aliases[x[0]].append(x[1])
                    aliases[x[1]].append(x[0])
                except Exception:
                    pass
            for x in self.links:
                for y in x[1:]:
                    e = aliases[y]
                    if e:
                        x.extend(e)

    def create_expression(self, expression):
        expr = Expression(expression, error=self.error)
        if 'delete' in dir(expr):
            return
        return expr

    def find_links(self, expression):
        expr = self.create_expression(expression)
        if expr is None: return
        for x in self.links:
            if expr.match(x[0]):
                yield x

    def find_referrers(self, expression):
        expr = self.create_expression(expression)
        if expr is None: return
        for x in self.links:
            for y in x[1:]:
                if expr.match(y):
                    yield x[0], y
