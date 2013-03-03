import epub, os
from genshi.template import TemplateLoader, MarkupTemplate
from epub import modulepath

class Section:

    def __init__(self):
        self.title = ''
        self.subsections = []
        self.css = ''
        self.text = []
        self.templateFileName = os.path.join(modulepath, 'templates/ez-section-mod.html')

class Book:

    def __init__(self):
        self.impl = epub.EpubBook()
        self.title = ''
        self.authors = []
        self.cover = ''
        self.lang = 'en-US'
        self.sections = []
	self.makefunc = {'plain': self.__addSection, 'html': self.__addHtmlSection}
        self.templateLoader = TemplateLoader('templates')
	if not os.path.exists(os.path.join('/tmp' , 'epub-builder')):
            os.makedirs(os.path.join('/tmp' , 'epub-builder'))

    def __addHtmlSection(self, section, id, depth):
        if depth > 0:
	    content = ''
	    for text in section.text:
	 	content = content + text
            urls = self.impl.downloadHtmlImages(content)
            content = self.impl.remoteToLocalImageUrls(urls, content)
            stream = MarkupTemplate("""<html xmlns="http://www.w3.org/1999/xhtml"
    					xmlns:py="http://genshi.edgewall.org/">
					<head>
					  <title>${section.title}</title>
					  <style type="text/css">
						h1 { text-align: center; }
						${section.css}
					  </style>
					</head>
					<body>
					  <h1>${section.title}</h1>
					  """ + content + """
					</body>
					</html>""").generate(section = section)
            html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)
            item = self.impl.addHtml('', '%s.html' % id, html)
            self.impl.addSpineItem(item)
            self.impl.addTocMapNode(item.destPath, section.title, depth)
            id += '.'
        if len(section.subsections) > 0:
            for i, subsection in enumerate(section.subsections):
                self.__addHtmlSection(subsection, id + str(i + 1), depth + 1)

    def __addSection(self, section, id, depth):
        if depth > 0:
            stream = self.templateLoader.load(section.templateFileName).generate(section = section)
            html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)
            item = self.impl.addHtml('', '%s.html' % id, html)
            self.impl.addSpineItem(item)
            self.impl.addTocMapNode(item.destPath, section.title, depth)
            id += '.'
        if len(section.subsections) > 0:
            for i, subsection in enumerate(section.subsections):
                self.__addSection(subsection, id + str(i + 1), depth + 1)

    def make(self, outputDir, type):

        outputFile = outputDir + '.epub'

        self.impl.setTitle(self.title)
        self.impl.setLang(self.lang)
        for author in self.authors:
            self.impl.addCreator(author)
        if self.cover:
            self.impl.addCover(self.cover)
        self.impl.addTitlePage()
        self.impl.addTocPage()
        root = Section()
        root.subsections = self.sections
        self.makefunc[type](root, 's', 0)
        self.impl.createBook()
        self.impl.createArchive(outputFile)
