#!/usr/bin/python
#coding=utf-8

import urllib2
import re
from lxml import etree

from bs4 import BeautifulSoup
url="http://www.weather.com.cn/weather/101190401.shtml"
request = urllib2.Request(url=url)
response = urllib2.urlopen(url,timeout=10)
html = response.read()
soup=BeautifulSoup(html,"lxml")
for link in soup.find_all("b7"):
  print(link)
