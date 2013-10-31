##
#    Project: RSStoEbook - Read your feeds on an ebook reader
#    Author: Andrea Bernardini <andrebask@gmail.com>
#    Copyright: 2012-2013 Andrea Bernardini
#    License: LGPL-3+
#
#    This file is part of RSStoEbook.
#
#    RSStoEbook is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RSStoEbook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with RSStoEbook.  If not, see <http://www.gnu.org/licenses/>.
##

from OPMLData import OPMLReader
from RSSData import RSSManager
from RSSData import FeedManager
from RSSData import DownloadedFeed
from EPubData import EPubGenerator
from PDFData import PDFGenerator
from ArticleData import ArticleExtractor
import sys, logging

version = '0.0.1'
usage = """RSStoEbook version %s
Copyright 2012-2013 Andrea Bernardini
License: LGPL-3+

Usage:

 rsstoebook <option> <url> -o <output_filename>

available options:

 -i    download articles importing RSS feeds from a list of opml files
 -f    download articles from a list of RSS feed urls
 -p    download articles from a list of webpage urls

supported output format: epub, pdf
           """ % version

if __name__ == "__main__":

    try: op = sys.argv[1]
    except: op = ''

    if op == '-i':
        opml_files = []
        end = sys.argv.index('-o')
        for arg in sys.argv[2:end]:
            opml_files.append(arg)
        feeds_urls = []
        for o in opml_files:
            feeds_urls.append(OPMLReader(o).get_feeds_urls())
        feeds = []
        for fu in feeds_urls:
            feeds.append((fu, "1970-01-01 00:00:00 UTC"))
        feeds = RSSManager(feeds).download_feeds()
        down_feeds = FeedManager(feeds).get_downloaded_feeds()
    elif op == '-f':
        feeds = []
        end = sys.argv.index('-o')
        for arg in sys.argv[2:end]:
            feeds.append((arg, "1970-01-01 00:00:00 UTC")
        feeds = RSSManager(feeds).download_feeds()
        down_feeds = FeedManager(feeds).get_downloaded_feeds()
    elif op == '-p':
        items = []
        end = sys.argv.index('-o')
        for arg in sys.argv[2:end]:
            items.append({'link': arg})
        articles = []
        for item in items:
            articles.append(ArticleExtractor().get_article_from_item(item))
        df = DownloadedFeed('', '', articles)
        down_feeds = [df]
    else:
        print usage

    for a in sys.argv:
        if a == '-o':
            out = sys.argv[sys.argv.index(a)+1]
            if out[out.rfind('.')+1:] == 'epub':
                EPubGenerator(down_feeds).generate_epub(out[:out.rfind('.')])
                sys.argv.remove(a)
            elif out[out.rfind('.')+1:] == 'pdf':
                PDFGenerator(down_feeds).generate_pdf(out[:out.rfind('.')])
                sys.argv.remove(a)
            continue
