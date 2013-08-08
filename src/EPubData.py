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
import os, re
#from epub_builder.ez_epub import Section, Book
from epub_builder.ez_epub import Section, Book

class EPubGenerator():

    def __init__(self, downloaded_feeds):
        self.downloaded_feeds = downloaded_feeds

    def generate_epub(self, filename):
        print 'generating epub book...'
        sections = []
        for feed in self.downloaded_feeds:
            if len(feed.articles) == 0:
                continue
            section = Section()
            section.title = feed.title
            subsections = []
            for article in feed.articles:
                subsection = Section()
                subsection.title = article.short_title
                subsection.text = [
                                   'Author: ' + article.author,

                                   article.clean_html_content
                                        .replace(article.short_title +'</h1>', '</h1>')
                                        .replace('<html>', '')
                                        .replace('</html>', '')
                                        .replace('<body/>', '')
                                   ]
                subsections.append(subsection)
            section.subsections = subsections
            sections.append(section)

        book = Book()
        book.title = 'News Feed'
        book.authors = ['RSStoEbook']
        book.sections = sections
        book.make(filename, 'html')
        print 'done.'

