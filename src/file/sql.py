#-*- coding:utf-8 -*-


import psycopg2
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def open_conn():
  conn = psycopg2.connect(database="dev", user="daqiang",
                          password="(LiHengShaui123)",
                          host="dev.cuauwtxtbfew.rds.cn-north-1.amazonaws.com.cn",
                          port="5432")
  return conn

def execute(sql):
  conn = open_conn()
  cur = conn.cursor();
  cur.execute(sql)
  rows = cur.fetchall()
  conn.close()
  return rows

def sel_desp_attname(tableName):
  sql ='  select a.attnum,'
  sql+='  (select description from pg_catalog.pg_description where objoid=a.attrelid and objsubid=a.attnum) as descript ,'
  sql+='  a.attname,pg_catalog.format_type(a.atttypid,a.atttypmod) as data_type '
  sql+='  from '
  sql+='  pg_catalog.pg_attribute a '
  sql+='  where '
  sql+='  1=1 '
  sql+='  and '
  sql+='  a.attrelid=(select oid from pg_class where relname=\'%s\') '
  sql+='  and '
  sql+='  a.attnum>0 '
  sql+='  and '
  sql+='  not a.attisdropped '
  sql+='  order by '
  sql+='  a.attnum;'
  return execute(sql%tableName)


def main():
  list =sel_desp_attname("t_manual");
  for line in list:
    for row in line:
      print(row)
if __name__ == '__main__':
  main()