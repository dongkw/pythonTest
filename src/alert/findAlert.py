# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
from PIL import Image
import pytesseract


def write_txt(txt):
  with open("log.txt", 'a') as f:
    print(txt + '\n')
    f.write(txt + '\n')


def findAlert(driver):
  try:
    a1 = driver.switch_to.alert  # 通过switch_to.alert切换到alert
    write_txt(a1.text)
    a1.accept()  # alert“确认”
  except:
    write_txt("无alert")
  sleep(10)


def main():
  driver = webdriver.Chrome()
  driver.set_window_size(1080, 800)
  driver.maximize_window()
  driver.get('http://cdmc.cep.webtrn.cn')
  driver.get_screenshot_as_file("clawerImgs/screenshot.png")
  while True:
    findAlert(driver)
  driver.quit()


def images(file):
  im = Image.open(file)
  imgry = im.convert('L')
  threshold = 140
  table = []
  for i in range(256):
    if i < threshold:
      table.append(0)
    else:
      table.append(1)
  out = imgry.point(table, '1')
  out.show()

  # print pytesser.image_file_to_string(out)
  tex = pytesseract.image_to_string(out)
  print(tex)


if __name__ == '__main__':
  images("1627.png")
