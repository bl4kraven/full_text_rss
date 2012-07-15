#!/usr/bin/env python
# -*-coding:UTF-8-*-
# api usage:
#     url=[rss url] -- the url convert to full txt rss.
#     key=[key] --  the password to create new feed.
#

import cgitb
cgitb.enable()

import cgi
form = cgi.FieldStorage();

from feedcache import Cache, RssWriter
import shelve
import sys

from config import *

def main():
    try:
        key = form.getfirst("key", None)
        url = form.getfirst("url", None)

        # verify the key
        is_key_valid = False
        if key and key in KEY_LIST:
            is_key_valid = True

        if not url:
            raise RuntimeError("api url is empty")

        storage = shelve.open('.feedcache')
        try:
            cache = Cache(storage, TIME_ZONE, TIMEOUT)
            rss = cache.fetch(url, is_key_valid)

            print "Content-type: application/atom+xml"
            print 
            rss.genarate_feed(sys.stdout)
        finally:
            storage.close()
    except RuntimeError:
        print 'Status: 400 Bad Request'
        print
        print 'Bad Request'

if __name__ == "__main__":
    main()
