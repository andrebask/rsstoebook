##
#    Project: RSStoEbook - Read your feeds on an ebook reader
#    Author: Andrea Bernardini <andrebask@gmail.com>
#    Copyright: 2012 Andrea Bernardini
#    License: GPL-3+
#
#    This file is part of RSStoEbook.
#
#    RSStoEbook is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RSStoEbook is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RSStoEbook.  If not, see <http://www.gnu.org/licenses/>.
##

from readability.readability import Document
import logging
import urllib

class ArticleExtractor():

    def get_article_from_item(self, item):
        url = item['link']
        logging.debug(url)
        author = 'n/a'
        if item.has_key('author'):
            author = item.author
        html = urllib.urlopen(url).read()
        doc = Document(html)
        return Article(doc.title(), doc.short_title(), author, doc.summary())

class Article():

    def __init__(self, title, short_title, author, clean_html_content):

        self.title = title
        self.short_title = short_title
        self.author = author
        self.clean_html_content = clean_html_content
