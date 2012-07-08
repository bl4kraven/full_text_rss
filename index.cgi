#!/usr/bin/env python
# -*-coding:UTF-8-*-

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage();

from feedcache import Cache, RssWriter
import shelve
import sys

def main():
    if "url" in form and (not isinstance(form["url"], list)):
        try:
            #url = "http://www.ftchinese.com/rss/news"
            storage = shelve.open('.feedcache')
            cache = Cache(storage)
            rss = cache.fetch(form["url"])

            print "Content-type: application/atom+xml"
            print 
            rss.genarate_feed(sys.stdout)
        finally:
            storage.close()
    else:
        pass

if __name__ == "__main__":
    main()
