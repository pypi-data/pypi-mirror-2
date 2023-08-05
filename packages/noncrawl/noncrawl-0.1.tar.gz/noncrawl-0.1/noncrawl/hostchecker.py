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

##[ Name        ]## hostchecker
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Checks if it's okay to crawl hosts
##[ Start date  ]## 2010 July 29

from datetime import datetime

get_seconds = lambda tdelta: tdelta.microseconds / 1000000.0
class HostChecker:
    def __init__(self, system, delay=0):
        self.system = system
        self.delay = delay
        if self.delay == 0:
            self.update = lambda now: None
        else:
            self.time = datetime.now()
            self.update = self._update

    def _update(self, now):
        self.delay -= get_seconds(now - self.time)
        if self.delay <= 0:
            for key, val in self.system.host_checks.items():
                if val == self:
                    del self.system.host_checks[key]
            return
        self.time = now
