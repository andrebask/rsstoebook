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

import os, HTMLParser, nltk, unicodedata
from ho.pisa import CreatePDF as to_pdf
#from xhtml2pdf.pisa import CreatePDF as to_pdf
class PDFGenerator():

    def __init__(self, downloaded_feeds):
        self.downloaded_feeds = downloaded_feeds
        self.title = 'News Feed'
        self.pageinfo = 'RSStoEbook'

    def generate_pdf(self, filename):
        finaltext = '<html>'
        for feed in self.downloaded_feeds:
            if len(feed.articles) == 0:
                continue
            finaltext += "<h1>%s</h1>\n" % feed.title
            for article in feed.articles:
                finaltext += "<h3>%s</h3>\n\n" % article.short_title
                finaltext += "Author: %s\n\n" % article.author
                finaltext += article.clean_html_content.replace(article.short_title +'</h1>', '</h1>').replace('<html>', '').replace('</html>', '').replace('<body/>', '').replace('a href=\"', 'a href=\"http://').replace('a href=\"http://http://', 'a href=\"http://')
        finaltext += '</html>'
	finaltext = unicodedata.normalize('NFKD', finaltext).encode('ascii','ignore')
        pdf = to_pdf(finaltext, file(filename, "wb"))
