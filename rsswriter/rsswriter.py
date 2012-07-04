#!/usr/bin/env python
# -*-coding:UTF-8-*-
# RSS 2.0 feed writer

from datetime import datetime
from rssitem import RssItem

class RssWriter():

    def __init__(self):
        # List of RssItem
        self.items = []
        self.channels = {}
        # set default value
        self.channels["title"] = "RSS 2.0 Feed"
        self.channels["description"] = "Full text rss"
        self.channels["generator"] = "http://www.freezhongzi.info"
        self.channels["link"] = ""
        self.channels["language"] = "zh"
        self.set_datetime("+0800")
        self.version = "2.0"

    def new_item(self):
	    # Create a new RssItem
		return RssItem()
	
    def add_item(self, feed_item):
	    # Add a FeedItem
		self.items.append(feed_item)

    def set_title(self, title):
        self.channels["title"] = title

    def set_link(self, link):
        self.channels["link"] = link

    def set_description(self, description):
        self.channels["description"] = description

    def set_datetime(self, time_zone):
        # Set pubDate and lastBuildDate with time zone
        rfc822time = "%a, %d %b %Y %H:%M:%S " + time_zone
        now = datetime.now()
        self.channels["pubDate"] = now.strftime(rfc822time)
        self.channels["lastBuildDate"] = self.channels["pubDate"]

    def get_datetime(self):
        return self.channels["pubDate"]

    def set_channels(self, key, value):
        self.channels[key] = value

    def print_head(self, fout):
		fout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		fout.write('<rss version="%s" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">\n' % self.version)

    def print_tale(self, fout):
        fout.write('</channel></rss>')

    def print_channels(self, fout):
        fout.write('<channel>\n')
        for key,value in self.channels.iteritems():
            # Encoding to utf-8
            value = value.encode("utf-8")
            fout.write('<%s>%s</%s>\n' % (key, value, key))

    def print_items(self, fout):
        for item in self.items:
            fout.write('<item>\n')
            for key,value in item.elements.iteritems():
                value = value.encode("utf-8")
                fout.write('<%s>%s</%s>\n' % (key, value, key))
            fout.write('</item>\n')

    def genarate_feed(self, fout):
        # Output the finally rss feed
		self.print_head(fout)
		self.print_channels(fout)
		self.print_items(fout)
		self.print_tale(fout)

if __name__ == "__main__":
    # Test
    rss = RssWriter()
    rss.set_title("RSS Test")
    rss.set_link("http://www.freezhongzi.info")
    rss.set_datetime("+0800")

    item = rss.new_item()
    item.set_title("test")
    item.set_link("http://www.freezhongzi.info")
    item.set_content(u"你好 world")
    rss.add_item(item)

    fout = open("test.xml", "w")
    rss.genarate_feed(fout)
