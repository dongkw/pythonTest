#!/usr/bin/python
# coding=utf-8

import csv
import urllib2
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def get_htm(url,head):
  browser = webdriver.Chrome()
  browser.get(url)



def seleniumz():
  browser = webdriver.Chrome()

  browser.get("http://www.baidu.com")
  print(browser.title)
  cookie=browser.get_cookies();
  print(cookie)
  time.sleep(5)
  # browser.find_element_by_id("kw").send_keys("selenium")
  # browser.find_element_by_id("su").click()
  browser.quit()



def get_html(url,head):


  request = urllib2.Request(url=url,headers=head)
  response = urllib2.urlopen(url, timeout=10)
  html = response.read()
  print(html)
  soup = BeautifulSoup(html, "lxml")
  return html


def get_data(html_text):
  final = []
  bs = BeautifulSoup(html_text, "lxml")  # 创建BeautifulSoup对象
  body = bs.body  # 获取body部分
  data = body.find('div', {'id': '7d'})  # 找到id为7d的div
  ul = data.find('ul')  # 获取ul部分
  li = ul.find_all('li')  # 获取所有的li

  for day in li:  # 对每个li标签中的内容进行遍历
    temp = []
    date = day.find('h1').string  # 找到日期
    temp.append(date)  # 添加到temp中
    inf = day.find_all('p')  # 找到li中的所有p标签
    temp.append(inf[0].string, )  # 第一个p标签中的内容（天气状况）加到temp中
    if inf[1].find('span') is None:
      temperature_highest = None  # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
    else:
      temperature_highest = inf[1].find('span').string  # 找到最高温
    temperature_lowest = inf[1].find('i').string  # 找到最低温
    temp.append(temperature_highest)  # 将最高温添加到temp中
    temp.append(temperature_lowest)  # 将最低温添加到temp中
    final.append(temp)  # 将temp加到final中

  return final


def write_cvs(data, name):
  csvf = file(name, "wb")

  wr = csv.writer(csvf)
  wr.writerow(['1', '2', '3', '4'])
  wr.writerows(data)
  csvf.close()


if __name__ == '__main__':
  seleniumz()
  # head = {"Accept": "application/json, text/plain, */*",
  #         "Accept-Encoding": "gzip, deflate",
  #         "Accept-Language": "zh-CN,zh;q=0.9",
  #         "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiJsTGtMQnIiLCJ1c2VyX25hbWUiOiIxNTkwMTU0ODUyMiIsInNjb3BlIjpbIkRPQ1RPUiJdLCJleHAiOjE1MTYwMDI2ODIsImF1dGhvcml0aWVzIjpbIlBBVElFTlRfUkVBRCIsIk1FU1NBR0VfUkVBRCIsIklNQUdFX1JFQUQiLCJRVUVTVElPTl9XUklURSIsIlJPTEVfQVNTSVNUQU5UIiwiTUVTU0FHRV9XUklURSIsIkFTU0lTVEFOVF9XUklURSIsIkFTU0lTVEFOVF9SRUFEIl0sImp0aSI6IjU2ODA1MjYwLWZiMmMtNDg3NS1iZGZiLThhZDE2NmZmMjRjMCIsImNsaWVudF9pZCI6ImRvY3Rvcl93ZWIifQ.Oc_0kb-C12EEzfqx3XQ_YrDmqYhwcyy_qgfVstHJ_0AKWWhqdrWQmXlXMeLKiWUbfetmaRc7lVx3ajmOOaglnA135cpta7MiVl7zVar7S8KyyW64NUbUd0hbz4SEN_6t4ofoqe7pV1wDewmryVEvliqNrZ27fmmEEfrkSO06H_hZWMhjnpDBnLajUjuxUj0okSTuWZ3kWSf6jJDZ_77-tlomJAuAX_NARuGl1rlfFVesFIX0oZ00AE8xi947X3Csz8K5XVkEqvQRGDQQdYaVIB41i31YZ4BHReQx3k9KbiGKl1xanNU75y9ffOp8WtHu-I7D8Mq1MRzirHAN6nMYVw",
  #         "Connection": "keep-alive",
  #         "Host": "devapi.xzlcorp.com:9004",
  #         "Origin": "http://xzl-doctor-web-dev.s3-website.cn-north-1.amazonaws.com.cn",
  #         "Referer": "http://xzl-doctor-web-dev.s3-website.cn-north-1.amazonaws.com.cn/",
  #         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
  #
  # url = 'http://xzl-doctor-web-dev.s3-website.cn-north-1.amazonaws.com.cn/#/doctor/patients?pageAt=0'
  # html = get_html(url,head)
  # result = get_data(html)
  # print(result);
  # write_cvs(result, 'weather.csv')
