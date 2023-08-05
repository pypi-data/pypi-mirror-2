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

##[ Name        ]## crawler
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls crawling
##[ Start date  ]## 2010 July 27

from urllib import FancyURLopener, unquote
class noncrawlOpener(FancyURLopener):
    version = 'Mozilla/5.0 (noncrawl/0.1)'

    def prompt_user_passwd(self, host, realm):
        user = 'admin'
        password = 'admin'
        return user, password

urllib = noncrawlOpener()
import re
import urlparse
try:
    from htmlentitiesdecode import decode as entity_decode
except ImportError:
    from noncrawl.external.htmlentitiesdecode import decode as entity_decode

from noncrawl.various import Container

INCORRECT = 0
UNKNOWN = 1
BLACKLISTED = 2

class Crawler:
    def __init__(self, supercrawler, *args, **kargs):
        self.supercrawler = supercrawler
        self.system = supercrawler.system
        self.protocol_regex = re.compile(r'.+?://.+')
        self.mailto_regex = re.compile(r'mailto:.+?@.+?')
        self.init(*args, **kargs)

    def __call__(self, url, info):
        urls = self.crawl(url, info)
        return tuple(set(urls))

    def crawl(self, content, info):
        pass

    def init(self, *args, **kargs):
        pass

    def improve_url(self, url, info):
        url = url.strip()
        strinfo = str(info)
        charset = strinfo.find('charset=')
        if charset != -1:
            e = strinfo.find('\n', charset + 8)
            if e != -1:
                charset = strinfo[charset + 8:e]
            else:
                charset = strinfo[charset + 8:]
            try:
                url = url.decode(charset, 'ignore')
            except Exception:
                pass
        url = unquote(url)
        try:
            url = entity_decode(url)
            url = url.encode('utf-8', 'ignore')
        except Exception:
            pass
        if self.mailto_regex.match(url):
            return
        url = urlparse.urlsplit(url).geturl()
        url = self.absolutify(url, info)
        s = url.find('//')
        e = url.rfind('/')
        if e == s + 1:
            url += '/'
        return url

    def absolutify(self, url, info):
        if self.protocol_regex.match(url):
            return url
        elif url.startswith('/'):
            return info.host + url
        elif url.startswith('#'):
            return info.rawurl + url
        elif url == '.' or url == '':
            return info.url
        elif url == '..':
            s = info.url.rfind('/')
            if s != -1:
                return info.url[:s + 1]
            else:
                return info.url
        else:
            path = info.path[:]
            if path.endswith('/'):
                path = path[:-1]
            while True:
                if url.startswith('..'):
                    url = url[2:]
                    if url.startswith('/'):
                        url = url[1:]
                    s = path.rfind('/')
                    if s != -1:
                        path = path[:s]
                elif url.startswith('.'):
                    url = url[1:]
                    if url.startswith('/'):
                        url = url[1:]
                else:
                    return path + '/' + url

from noncrawl.crawlers import *
class SuperCrawler:
    def __init__(self, system, blacklist=None):
        self.system = system
        self.blacklist = blacklist
        self.crawler = Container()
        self.crawler.html = htmlcrawler.HTMLCrawler(self)

    def __call__(self, address):
        if not self.system.whiteblacklist.is_ok(address):
            return BLACKLISTED
        try:
            return self.crawl(address)
        except Exception, error:
            self.system.error(repr(error))
            if 'url error' in error:
                # This is fatal
                return INCORRECT
            else:
                # Only slighty fatal
                return UNKNOWN

    def crawl(self, address):
        page = urllib.open(address)
        info = page.info()
        info.url = page.url
        ss = info.url.find('//')
        s = info.url.find('/', ss + 2)
        if s != -1:
            info.host = info.url[:s]
        else:
            info.host = info.url
        e = info.url.rfind('/')
        if e != ss + 1:
            info.path = info.url[:e + 1]
        else:
            info.url += '/'
            info.path = info.url

        info.rawurl = info.url[:]
        s = info.rawurl.find('#')
        if s != -1:
            info.rawurl = info.rawurl[:s]
        info.crawl = lambda: self.do_crawl(page, info)
        return info

    def do_crawl(self, page, info):
        subtype = info.getsubtype()
        if subtype == 'html':
            links = self.crawler.html(page.read(), info)
        else:
            links = []
        return links
