#!/usr/bin/env python
# -*-coding:UTF-8-*-
# RSS 2.0 item class

class RssItem():

    def __init__(self):
        self.elements = {}

    def set_title(self, title):
        self.elements["title"] = "<![CDATA[" + title + "]]>"

    def set_link(self, link):
        self.elements["link"] = link

    def set_guid(self, guid):
        self.elements["guid"] = guid

    def set_description(self, description):
        self.elements["description"] = "<![CDATA[" + description + "]]>"

    def set_content(self, content):
        # Content is in content:encoded
        self.elements["content:encoded"] = "<![CDATA[" + content + "]]>"

    def set_datetime(self, date):
        self.elements["pubDate"] = date

    def set_elements(self, key, value):
        self.elements[key] = value

    def get_guid(self):
        return self.elements.get("guid", None)
    
    def get_content(self):
        return self.elements.get("content:encoded", None)
