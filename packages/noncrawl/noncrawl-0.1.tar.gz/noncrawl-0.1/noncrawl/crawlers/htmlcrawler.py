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

##[ Name        ]## htmlcrawler
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Crawls HTML pages
##[ Start date  ]## 2010 July 27

import re
from noncrawl.crawler import Crawler

class HTMLCrawler(Crawler):
    def init(self):
        flags = re.IGNORECASE | re.DOTALL
        self.regexes = []
        for t in ('"', "'"):
            # <a href="...">, <img src='...' /> etc.
            self.regexes.append([
                re.compile(r'<[a-z]+\s+(href|src)=%s(.*?)%s.*?>' %
                           (t, t), flags), 1])

            # CSS' url("...")
            self.regexes.append([
                re.compile(r'(url\s*\(\s*%s(.*?)%s\s*\))' % (t, t),
                           flags), 1])
        self.regexes.append([re.compile(r'''(url\s*\(\s*([^"']*?)\s*\))''', flags), 1])

        # Urls in clear text
        self.regexes.append((re.compile(
                    r'''((http|https|ftp)://.+?(?=["',;<>\)\]\}\s]))''',
                    flags), 0))
        # Urls in clear text without the http://
        self.www_reg = \
            re.compile(r'''(www\.(.*?\..*?)+?.*?)(?=["',;<>\)\]\}\s])''',
                       flags)

    def crawl(self, content, info):
        links = []
        for r in self.regexes:
            links.extend([l[r[1]] for l in r[0].findall(content)])
        links.extend(['http://' + l[0] for l in
                      self.www_reg.findall(content)])
        nlinks = []
        for l in links:
            i = self.improve_url(l, info)
            if i:
                nlinks.append(i)
        return nlinks
