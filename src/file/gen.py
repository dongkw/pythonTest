# -*- coding:utf-8 -*-
from shutil import copy
import sys
import re
import os
import sql

reload(sys)
sys.setdefaultencoding('utf-8')

list = []
table_name = "t_basic_hospital"


def read_file(file):
  file_obj = open(file, "rb")
  try:
    file_text = file_obj.read()
  finally:
    file_obj.close()
  return file_text


def write_file(target_file, file_text):
  with open(target_file, "wb") as f:
    f.write(file_text)


def copy_files(source_dir, dest_dir):
  for file in os.listdir(source_dir):
    source_file = os.path.join(source_dir, file)
    target_file = os.path.join(dest_dir, file)
    if os.path.isfile(source_file):
      if not os.path.exists(target_file):
        if not os.path.exists(dest_dir):
          os.makedirs(dest_dir)
      # if not os.path.exists(target_file) or (os.path.exists(target_file) and (
      #     os.path.getsize(target_file) != os.path.getsize(source_file))):
      if('dev' in source_file):
        change_file(target_file, source_file)
    if os.path.isdir(source_file):
      copy_files(source_file, target_file)


def change_file(target_file, source_file):
  file_text = read_file(source_file)
  write_file(re_yml_name(target_file), file_text)

def name_list():
  if len(list)<=0:
    name = re.findall('_\S', table_name)
    name2 = re.split('_\S', table_name)
    className = ''
    for i in range(0, len(name2) - 1):
      className = str(name[i].upper()[1:]) + name2[i + 1]
    list.append(className)
    list.append(table_name.replace('t_', '').replace('_', '-'))
    list.append(className.replace(className[:1],str(className[:1]).lower()))
  return list
def re_yml_name(name):
  print(name)
  name=name.replace("dev","test")
  print(name)
  return name
def target_name(target_file):
  className=''
  if (target_file.endswith('.java')):
    className= list[0]
  if (target_file.endswith('.html')):
    className= list[1]
  target_file = target_file.replace("{table}", className)
  return target_file


def main():
  path = os.getcwd()
  print(os.listdir(path))
  source_dir = '/Users/xinzhilimacpro/workspace/config-repo'
  dest_dir = '/Users/xinzhilimacpro/workspace/config-repo'
  name_list()
  copy_files(source_dir, dest_dir)

  # print(sql.sel_desp_attname("t_basic_hospital"))


if __name__ == '__main__':
  main()
