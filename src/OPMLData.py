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

import listparser

class OPMLReader():

    def __init__(self, opml_file):

        print "reading opml file..."

        self.info = listparser.parse(opml_file)
        self.feeds = self.info.feeds

        print self.info.meta.title
        print self.info.meta.created

    def get_feeds_urls(self):
        urls = []
        for feed in self.info.feeds:
            urls.append(feed.url)
        return urls





