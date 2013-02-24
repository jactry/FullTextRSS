#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, urllib2
import re
import datetime
import PyRSS2Gen
import codecs


try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def zh2unicode(str): 
    for c in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr','utf16','utf32'): 
        encc = c 
        try: 
            return str.decode(c) 
        except: 
            pass 
    return str

def get_content(link, begin_tag, end_tag):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
    req = urllib2.Request(
        url = link,
        headers = headers
        )
    try:
        html = zh2unicode(urllib2.urlopen(req).read())
    except urllib2.HTTPError:
        html = link
    try:
        m = html.index(begin_tag)
        n = html.index(end_tag)
    except ValueError:
        return link
    return html[m:n]

def gen_item(post_title, post_link, post_content):
    item = PyRSS2Gen.RSSItem(
        title = post_title,
        link = post_link,
        description = post_content,)
    return item

def gen_rss(site_title, site_link, site_desp, site_items, rssname):
    rss = PyRSS2Gen.RSS2(
        title = site_title,
        link = site_link,
        description = site_desp,
        lastBuildDate = datetime.datetime.now(),
        items = site_items,)
    rss.write_xml(open('rss/'+ rssname + '.xml', 'w'), encoding='utf-8')
    
def get_rss(rss_link, begin_tag, end_tag, rssname):
    xml = urllib2.urlopen(rss_link).read()
    f = open('feed.xml', 'w')
    f.write(xml)
    f.close()
    tree = ET.ElementTree(file='./feed.xml')
    root = tree.getroot()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    site_title = ""
    site_link = ""
    site_desp = ""
    post_title = ""
    post_link = ""
    post_content = ""
    site_items = []
    for child in root[0]:
        if child.tag == "title":
            site_title = child.text
        elif child.tag == "link":
            site_link = child.text
        elif child == "description":
            site_desp = child.text
        elif child.tag == "item":
            for element in child:
                if element.tag == "title":
                    post_title = element.text
                elif element.tag == "link":
                    print element.text
                    post_link = element.text
                    post_content = get_content(post_link, begin_tag, end_tag)

            item = gen_item(post_title, post_link, post_content)
            site_items.append(item)

    gen_rss(site_title, site_link, site_desp, site_items, rssname)
