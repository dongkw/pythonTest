# -*- coding:utf-8 -*-

from selenium import webdriver
from time import sleep
from PIL import Image
import pytesseract

SCREEN = "clawerImgs/screenshot.png"
VALIDATE = "clawerImgs/verification.png"

driver = webdriver.Chrome()
driver.set_window_size(1080, 800)
driver.maximize_window()
driver.get('http://cdmc.cep.webtrn.cn')
USER_NAME = 'C171110603617'
PASSWORD = '111111'
AUTO_TIME = 10


def write_txt(txt):
  with open("log.txt", 'a') as f:
    print(txt + '\n')
    f.write(txt + '\n')


def findAlert():
  # 找到所有标签页
  handles = driver.window_handles

  for newhandle in handles:
    sleep(AUTO_TIME)
    driver.switch_to.window(newhandle)
    try:
      play()
    except:
      write_txt("找不到按钮")
    try:
      alert()
    except:
      write_txt("现在无alert")
    driver.switch_to.parent_frame()


# 模拟点击alert
def alert():
  driver.switch_to.frame('scormContent')
  driver.switch_to.frame(0)
  a1 = driver.switch_to.alert  # 通过switch_to.alert切换到alert
  a1.accept()


# 如果没有播放则播放视频
def play():
  driver.switch_to.frame('scormContent')
  driver.switch_to.frame(0)
  play = driver.find_element_by_id('flash_player_display_button')
  playStyle = play.get_attribute('style') + ""
  if (playStyle.find("opacity: 0;")):
    write_txt("视频未自动播放 ---点击播放")
    play.click()


def main():
  login()
  sleep(2)
  study()

  while True:
    findAlert()
  driver.quit()


def study():
  imgs = driver.find_elements_by_class_name('img')
  for img in imgs:
    sleep(1)
    img.click()


def login():
  code = get_code()
  driver.switch_to.frame('center')
  user = driver.find_element_by_id('loginId')
  pwd = driver.find_element_by_id('passwd')
  autoCode = driver.find_element_by_id('authCode')
  Login_btn = driver.find_element_by_id('Login_btn')

  user.send_keys(USER_NAME)
  pwd.send_keys(PASSWORD)
  autoCode.send_keys(code)
  Login_btn.click();


# 获取验证码
def get_code():
  sleep(0.5)
  driver.get_screenshot_as_file(SCREEN)
  crop_image(SCREEN)
  code = images(VALIDATE)
  return code

  # 找到验证码


def crop_image(file):
  x = 385
  y = 870
  w = 120
  h = 40
  im = Image.open(file)
  img = im.crop((x, y, x + w, y + h))
  img.save(VALIDATE)
  # img.show()
  return img


# 把图片变为数字
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
  # out.show()
  tex = pytesseract.image_to_string(out)
  return tex


if __name__ == '__main__':
  main()
