#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@author: g3rhard
inspired by https://github.com/rocco66/getnota/
Requirements:
    lxml
    python3
'''

import requests
import sys

import lxml.html
from lxml.etree import tostring
from lxml.html import parse
from lxml import etree


USERNAME = sys.argv[1];
PASSWORD = sys.argv[2];
BOOKID = sys.argv[3];

LOGINURL = 'http://notabenoid.org'
DATAURL = 'http://notabenoid.org/book/'

BOOK_INFO_ID = 'Info'
CHAP_LIST_ID = 'Chapters'
CONTENT_ID = 'content'

session = requests.session()

req_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
}

formdata = {
    'login[login]': USERNAME,
    'login[pass]': PASSWORD
}

# Authenticate
auth = session.post(LOGINURL, data=formdata, headers=req_headers, allow_redirects=False)

# Read data
book_page = session.get(DATAURL+BOOKID)

page = lxml.html.fromstring(book_page.text)
title = page.xpath('/html/body/div[3]/div[2]/div[1]/h1/text()')[0]
print("# " + title)

# Get pages
xpath_pages = '//*[@id="Chapters"]/tbody/tr[*]/td[5]/a/@href'
pages = page.xpath(xpath_pages)

for p in pages:
    # print(LOGINURL + p)
    xpath_text = '/html/body/div[3]/div[2]/div[1]'
    xpath_title = '/html/body/div[3]/div[2]/div[1]/h1/text()'
    chapter_page = session.get(LOGINURL + p)
    chapter_text = lxml.html.fromstring(chapter_page.text)
# Chapter
    chapter_title = chapter_text.xpath(xpath_title)[0]
    print("## " + chapter_title )
# Paragraph
    text_block = chapter_text.xpath(xpath_text)
    for paragraph in text_block:
        print(paragraph.text_content())
