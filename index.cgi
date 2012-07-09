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
    if "url" in form and (not isinstance(form.getvalue("url"), list)):
        #try:
        storage = shelve.open('.feedcache')
        cache = Cache(storage)
        rss = cache.fetch(form.getvalue("url"))

        print "Content-type: application/atom+xml"
        print 
        rss.genarate_feed(sys.stdout)
        #finally:
        storage.close()
    else:
        print 'Status: 400 Bad Request'
        print

if __name__ == "__main__":
    main()
