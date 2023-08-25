# -*- coding:utf-8 -*-

import psycopg2
import xdrlib, sys
import xlrd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def open_excel(file):
  data = xlrd.open_workbook(file)
  return data


def open_pg_database():
  conn = psycopg2.connect(database="dev", user="daqiang",
                          password="(LiHengShaui123)",
                          host="dev.cuauwtxtbfew.rds.cn-north-1.amazonaws.com.cn",
                          port="5432")
  return conn


def select(sql):
  conn = open_pg_database()
  cur = conn.cursor()
  cur.execute(sql)
  rows = cur.fetchall()
  conn.close()
  return rows


def excal_table_byindex(file="1.xlsx", colnameindex=1, by_index=0):
  data = open_excel(file)
  table = data.sheets()[by_index]
  # table=data.sheet_by_name("Sheet2")
  nrows = table.nrows
  ncols = table.ncols
  colnames = table.row_values(colnameindex)
  list = []
  clean()

  for rownum in range(1, nrows):
    row = table.row_values(rownum)
    if row[1]!='':

      sql= 'update s_medical.t_inspection_reference set name= \''+row[2]+'\' where name=\''+row[1]+'\';\n'
      write_txt(sql)
      insert(sql)
      sql2= 'update s_medical.t_inspection_record set name= \''+row[2]+'\' where name=\''+row[1]+'\';\n'
      write_txt(sql2)
      insert(sql2)
def clean():
  with open("1.txt", 'w') as f:
    f.write("")


def write_txt(txt):
  with open("1.txt", 'a') as f:
    print(txt)
    f.write(txt)


def insert(txt):
  conn = open_pg_database()
  cur = conn.cursor()
  cur.execute(txt)
  conn.commit()
  conn.close()


def main():
  excal_table_byindex()


if __name__ == '__main__':
  main()
