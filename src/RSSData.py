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

import feedparser
import threading
from datetime import datetime, timedelta
from ArticleData import ArticleExtractor

class RSSManager():

    threads_num = 4
    feed_list = []

    def __init__(self, url_list):

        self.feed_url_list = url_list
        self.slot = len(url_list)/self.threads_num

    def download_feeds(self):
        print 'downloading feed list...'
        for i in range(1,self.threads_num):
            urls = self.feed_url_list[ (i-1) * self.slot : i * self.slot ]
            if len(urls) > 0:
                threading.Thread(target=self.__download, args=(urls,)).start()
        urls = self.feed_url_list[ self.slot * (self.threads_num-1) : ]
        if len(urls) > 0:
            threading.Thread(target=self.__download, args=(urls,)).start()

        for thread in threading.enumerate():
            if thread is not threading.currentThread():
                thread.join()

        return self.feed_list

    def __download(self, urls):
        for url in urls:
            feeddata = feedparser.parse(url)
            try:
                feed = Feed(feeddata['channel']['title'],
                            feeddata['channel']['description'],
                            feeddata['items'])
            except:
                feed = Feed(feeddata['url'],
                            '',
                            feeddata['items'])
            self.feed_list.append(feed)

class FeedManager():

    threads_num = 4

    def __init__(self, feed_list):
        self.feed_list = feed_list
        self.downloaded_feed_list = []
        self.tmp_articles = []
        self.slot = len(feed_list)/self.threads_num

    def get_downloaded_feeds(self):
        print 'downloading feed contents...'
        self.downloaded_feed_list = []
        j=0
        for feed in self.feed_list:
            self.tmp_articles = []
            item_list = feed.items
            for i in range(1,self.threads_num):
                feed_items = item_list[ (i-1) * self.slot : i * self.slot ]
                if len(feed_items) > 0:
                    threading.Thread(target=self.__download_articles, args=(feed_items,)).start()
            feed_items = item_list[ self.slot * (self.threads_num-1) : ]
            if len(feed_items) > 0:
                threading.Thread(target=self.__download_articles, args=(feed_items,)).start()

            for thread in threading.enumerate():
                if thread is not threading.currentThread():
                    thread.join()
            j = j+1
            print 'content of '+ str(j) + ' of ' + str(len(self.feed_list)) + ' feeds downloaded'
            self.downloaded_feed_list.append(DownloadedFeed(feed.title, feed.description, self.tmp_articles))

        return self.downloaded_feed_list

    def __download_articles(self, feedItems):
        for item in feedItems:
            now = datetime.now()
            yesterday = now - timedelta(days=1.5)
            try:
                if item['date_parsed'] > yesterday.timetuple():
                    self.tmp_articles.append(ArticleExtractor().get_article_from_item(item))
            except:
                self.tmp_articles.append(ArticleExtractor().get_article_from_item(item))

class AbstractFeed():

    def __init__(self, title, description):

        self.title = title
        self.description = description

class Feed(AbstractFeed):

    def __init__(self, title, description, items):

        AbstractFeed.__init__(self, title, description)
        self.items = items

class DownloadedFeed(AbstractFeed):

    def __init__(self, title, description, articles):

        AbstractFeed.__init__(self, title, description)
        self.articles = articles
