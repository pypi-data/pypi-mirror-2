#!/usr/bin/env python
from distutils.core import setup
import noncrawl.generalinformation as ginfo

readme=open('README.txt').read()
conf = dict(
    name='noncrawl',
    version=ginfo.version,
    author='Niels Serup',
    author_email='ns@metanohi.org',
    packages=['noncrawl', 'noncrawl.crawlers', 'noncrawl.external'],
    scripts=['noncrawler', 'noncrawlget'],
    requires=['htmlentitiesdecode'],
    url='http://metanohi.org/projects/noncrawl/',
    license='LICENSE.txt',
    description='A web crawler creating link soups',
    classifiers=['Development Status :: 2 - Pre-Alpha',
                 'Intended Audience :: End Users/Desktop',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: GNU General Public License (GPL)',
                 'License :: DFSG approved',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'
                 ]
)

try:
    # setup.py register wants unicode data..
    conf['long_description'] = readme.decode('utf-8')
    setup(**conf)
except Exception:
    # ..but setup.py sdist upload wants byte data
    conf['long_description'] = readme
    setup(**conf)
