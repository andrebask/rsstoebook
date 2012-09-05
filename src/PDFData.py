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

import os, HTMLParser, nltk
from xhtml2pdf.pisa import CreatePDF as to_pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

PAGE_HEIGHT=A4[1]
PAGE_WIDTH=A4[0]
styles = getSampleStyleSheet()

class PDFGenerator():

    def __init__(self, downloaded_feeds):
        self.downloaded_feeds = downloaded_feeds
        self.title = 'News Feed'
        self.pageinfo = 'RSStoEbook'

    def first_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold',28)
        canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, self.title)
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "First Page / %s" % self.pageinfo)
        canvas.restoreState()

    def later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman',9)
        canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, self.pageinfo))
        canvas.restoreState()

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
        pdf = to_pdf(
            finaltext,
            file(filename, "wb"))
        #if not pdf.err:
         #   xhtml2pdf.startViewer(filename)

    def generate_pdf_rp(self, filename):
        doc = SimpleDocTemplate(os.path.join(os.environ.get('HOME', None) , 'Scaricati', filename + '.pdf'))
        Story = [Spacer(1,2*inch)]
        print 'generating pdf...'
        for feed in self.downloaded_feeds:
            if len(feed.articles) == 0:
                continue
            if len(feed.title) != 0:
                p = Paragraph(feed.title, styles["Heading1"])
                Story.append(p)
                Story.append(Spacer(1,0.2*inch))

            for article in feed.articles:

                p = Paragraph(article.short_title, styles["Heading3"])
                Story.append(p)
                Story.append(Spacer(1,0.2*inch))

                p = Paragraph('Author: ' + article.author, styles["Normal"])
                Story.append(p)
                Story.append(Spacer(1,0.2*inch))

                try:

                    h = HTMLParser.HTMLParser()
                    text = h.unescape(article.clean_html_content
                                       .replace(article.short_title +'</h1>', '</h1>')
                                       .replace('<html>', '')
                                       .replace('</html>', '')
                                       .replace('<body/>', '')
                                       .replace('a href=\"', 'a href=\"http://')
                                       .replace('a href=\"http://http://', 'a href=\"http://'))
                    p = Paragraph(text, styles["Normal"])

                except:

                    print 'WARNING: can\'t process \"' + article.short_title + '\"with html \n using plain text instead\n\n'
                    text = nltk.clean_html(article.clean_html_content
                                           .replace(article.short_title +'</h1>', '</h1>'))
                    p = Paragraph(text, styles["Normal"])

                Story.append(p)
                Story.append(Spacer(1,0.2*inch))

        doc.build(Story, onFirstPage=self.first_page, onLaterPages=self.later_pages)

        print 'done.'
