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

##[ Name        ]## system
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Controls everything
##[ Start date  ]## 2010 July 27

import os
import re
from datetime import datetime
import time

import noncrawl.crawler as crawler
urllib = crawler.urllib
import noncrawl.various as various
from noncrawl.hostchecker import HostChecker
from noncrawl.statusprinter import StatusPrinter
import noncrawl.whiteblacklist as whiteblacklist

class System(object):
    def __init__(self, etc, error=None):
        for x in eval(str(etc)).items():
            self.__setattr__(*x)

        if error is None:
            self.error = various.usable_error
        else:
            self.error = error

        self.status = StatusPrinter(self, 'noncrawl', 'red', 'blue')
        self.status('''\
noncrawl is free software: you are free to change and redistribute it
under the terms of the GNU GPL, version 3 or any later version.
There is NO WARRANTY, to the extent permitted by law. See
<http://metanohi.org/projects/noncrawl/> for downloads and documentation.''')

    def start(self):
        self.status('Starting noncrawl...')
        if self.whiteblacklist:
            self.whiteblacklist = whiteblacklist.List(
                self, file=self.whiteblacklist,
                ignore_base=not self.use_base_list)
        else:
            self.whiteblacklist = whiteblacklist.List(
                self, ignore_base=not self.use_base_list)
        self.new_crawl = crawler.SuperCrawler(self)

        self.host_checks = {}
        self.host_delays = {}

        self.testurls = []
        self.visited = []
        self.visited_num = 0

        if self.use_threads:
            self.threads_running = 0

        if self.load_from:
            self.load_project()
            return

        if not self.is_recursive:
            self.end = lambda: None
            for x in self.startpages:
                info = self.new_crawl(x)
                if info in (crawler.INCORRECT, crawler.UNKNOWN,
                            crawler.BLACKLISTED):
                    self.error('url "%s" is not accesible, ignoring' % x)
                    continue
                print 'Checking "%s"...' % info.url
                links = info.crawl()
                for y in links:
                    print 'Found %s' % y
                print

            print 'Done.'
            return

        self.new_project()

    def new_project(self):
        if not self.startpages:
            self.error('you must specify at least one web address as a \
starting point for your link crawl', False)

        if self.project_name:
            name = self.project_name
        else:
            name = 'noncrawl-results'
        orig_name = name[:]
        while os.path.exists(name):
            name = '_' + name
        if not orig_name == name:
            self.error('project named "%s" already exists, \
renaming to "%s"' % (orig_name, name))
        try:
            os.mkdir(name)
            os.chdir(name)
            self.linksfile = open('links', 'w')
            self.aliasfile = open('aliases', 'w')
            self.visitedfile = open('visited', 'w')
        except Exception, error:
            self.error(error, False)

        self.testurls = self.startpages[:]
        self.visited = []
        self.visited_num = 0
        self.run()

    def load_project(self, name=None):
        name = name or self.load_from
        try:
            os.chdir(name)
            self.linksfile = open('links', 'a')
            self.aliasfile = open('aliases', 'a')
            self.visited = []
            with open('visited', 'r') as f:
                for line in f:
                    self.visited.append(line[:-1])
            self.visitedfile = open('visited', 'a')
            self.visited_num = int(open('total_visits', 'r').read())
            self.testurls = []
            with open('urls_not_crawled', 'r') as f:
                for line in f:
                    self.testurls.append(line[:-1])
        except Exception, error:
            self.error(error, False)

        self.run()

    def save_project(self):
        f = open('urls_not_crawled', 'w')
        for url in self.testurls:
            f.write(url)
            f.write('\n')
        f = open('total_visits', 'w')
        f.write(str(self.visited_num))

    def parse_robots(self, url, prop):
        try:
            text = urllib.open(url).read()
        except Exception:
            return
        m = re.search(r'[\n\r][\s#]*' + prop + r':\s*(.+)', text)
        if m:
            return m.group(1)

    def get_crawl_delay(self, url):
        s = url.find('/', url.find('//') + 2)
        if s != -1:
            host = url[:s + 1]
        else:
            host = url + '/'
        try:
            return self.host_checks[host].delay
        except KeyError:
            try:
                delay = self.host_delays[host]
            except KeyError:
                delay = self.parse_robots(
                        host + 'robots.txt', 'Crawl-delay')
                if delay:
                    try:
                        delay = int(delay)
                    except ValueError:
                        delay = 0
                else:
                    delay = 0
            self.host_delays[host] = delay
            self.host_checks[host] = HostChecker(self, delay)
            return 0

    def thread_func(self, func, *args):
        func(*args)
        self.threads_running -= 1

    def new_thread(self, *args):
        t = various.thread(self.thread_func, *args)
        self.threads_running += 1

    def add_alias(self, url1, url2):
        self.aliasfile.write(url1 + '\n' + url2 + '\n\n')

    def add_visited_to_file(self, url):
        self.visitedfile.write(url + '\n')

    def add_links(self, url, links):
        text = url
        for link in links:
            text += '\n' + link
        self.linksfile.write(text + '\n\n')

        self.testurls.extend(links)

    def test_url_in_thread(self, url):
        self.pre_test_url(url, lambda: self.new_thread(self.do_test_url, url))

    def test_url(self, url):
        self.pre_test_url(url, lambda: self.do_test_url(url))

    def pre_test_url(self, url, func):
        self.testurls.remove(url)
        if url in self.visited:
            return
        self.visited.append(url)
        func()

    def do_test_url(self, url):
        delay = self.get_crawl_delay(url)
        if delay:
            time.sleep(delay)

        info = self.new_crawl(url)
        if info == crawler.INCORRECT:
            self.error('"%s" is not a real url; will not try again \
later' % url)
            return
        elif info == crawler.BLACKLISTED:
            return
        if info == crawler.UNKNOWN:
            self.error('url "%s" is not accesible now; will try again \
later' % url)
            self.testurls.append(url)
            self.visited.remove(url)
            return

        self.add_visited_to_file(url)
        self.visited_num += 1

        if info.url != url and info.url in self.visited:
            return
        if info.rawurl != url and info.rawurl in self.visited:
            return
        if url != info.url:
            self.visited.append(info.url)
            self.add_visited_to_file(info.url)
            self.add_alias(url, info.url)
        if url != info.rawurl != info.url:
            self.visited.append(info.rawurl)
            self.add_visited_to_file(info.rawurl)
            self.add_alias(url, info.rawurl)
            if info.url != url:
                self.add_alias(info.url, info.rawurl)
        links = info.crawl()
        print 'Found %d links on %s' % (len(links), info.url)
        self.add_links(info.url, links)

    def run(self):
        if not self.use_threads:
            while True:
                self.test_url(self.testurls[0])
                now = datetime.now()
                for x in self.host_checks.values():
                    x.update(now)
                if self.visited_num >= self.max_visits or \
                        len(self.testurls) == 0:
                    break
                time.sleep(0.01)
        else:
            while True:
                if self.threads_running == 0 and \
                        len(self.testurls) == 0:
                    break
                max_num = self.thread_limit - self.threads_running
                if max_num == 0:
                    time.sleep(0.01)
                    continue
                testurls = self.testurls[:max_num]
                for url in testurls:
                    self.test_url_in_thread(url)
                now = datetime.now()
                for x in self.host_checks.values():
                    x.update(now)
                if self.visited_num >= self.max_visits:
                    break
                time.sleep(0.01)

    def exit(self):
        sys.exit()

    def end(self):
        if self.use_threads:
            t = 0
            try:
                while self.threads_running > 0:
                    s = self.threads_running > 1 and 's' or ''
                    print 'Shutting down, waiting for \
%d thread%s to finish...' % (self.threads_running, s)
                    time.sleep(1.0)
                    t += 1
                    if t > 100:
                        # We're not waiting for more than >100+ seconds
                        raise KeyboardInterrupt
            except KeyboardInterrupt:
                print 'Ignoring waiting.'
        try:
            self.status('Saving project...')
            self.save_project()
        except KeyboardInterrupt:
            try:
                self.status('Not so fast! Saving project...')
                self.save_project()
            except KeyboardInterrupt:
                print 'OK, quitting.'
