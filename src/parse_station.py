import re
import urllib2
from pprint import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
response = urllib2.urlopen(url)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.read())
pprint(dict(stations), indent=4)