rsstoebook
==========
Read your feeds on an ebook reader

Copyright: 2012-2013 Andrea Bernardini

License: LGPL-3+

Can be used as a python module or a command line application.

####Usage:####

rsstoebook OPTION URL ... -o OUTPUT_FILENAME

available options:

 -i download articles importing RSS feeds from a list of opml files  
 -f download articles from a list of RSS feed urls  
 -p download articles from a list of webpage urls

supported output format: epub, pdf

####Requirements:####

python-listparser  
python-feedparser  
python-genshi  
python-cssselect  
python-readability  
python-xhtml2pdf (python-pisa)  
python-nltk  
epub-builder (https://github.com/andrebask/epub-builder)
