#!/USR/BIN/env python
# -*-coding:UTF-8-*-

import urllib2
from readability.readability import Document
import feedparser
from rsswriter import RssWriter,RssItem

from config import *

def main():
    url = "http://www.ftchinese.com/rss/news"
    #url = "http://cppblog.com/rss.aspx"
    rss_file = urllib2.urlopen(url, timeout=TIMEOUT).read()
    print "parsering"
    rss_read = feedparser.parse(rss_file)
    print "parse complete"
    if not rss_read.version:
        raise "Unknown feed type" 

    print rss_read.feed.title, rss_read.feed.description
    print rss_read.feed.link
    print

    # full text rss output
    full_text_rss = RssWriter()
    full_text_rss.set_title(rss_read.feed.title)
    full_text_rss.set_link(rss_read.feed.link)
    full_text_rss.set_description(rss_read.feed.description)
    full_text_rss.set_datetime(TIME_ZONE)

    # set item
    for item in rss_read.entries:
        print item.title
        if item.has_key("content"):
            raise "Already a full feed text"

        full_text_item = full_text_rss.new_item()
        full_text_item.set_title(item.title)
        full_text_item.set_link(item.link)

        if item.has_key("guid"):
            full_text_item.set_guid(item.guid)
        else:
            full_text_item.set_guid(item.link)

        if item.has_key("published"):
            full_text_item.set_datetime(item.published)
        else:
            full_text_item.set_datetime(full_text_rss.get_datetime())

        try:
            print "http read item link", item.link
            # timeout 
            html = urllib2.urlopen(item.link, timeout=TIMEOUT).read()
            readable_article = Document(html).summary()
        except IOError:
            readable_article = ""

        full_text_item.set_content(readable_article)
        full_text_rss.add_item(full_text_item)

    output = open("test.xml", "w")
    full_text_rss.genarate_feed(output)

if __name__ == "__main__":
    main()
