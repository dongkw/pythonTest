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
  cur = conn.cursor();
  cur.execute(sql)
  rows = cur.fetchall()
  conn.close()
  return rows


def excal_table_byindex(file="xl1.4.xlsx", colnameindex=1, by_index=0):
  data = open_excel(file)
  table = data.sheets()[by_index]
  # table=data.sheet_by_name("Sheet2")
  nrows = table.nrows
  ncols = table.ncols
  colnames = table.row_values(colnameindex)
  list = []
  clean()

  for rownum in range(0, nrows):
    row = table.row_values(rownum)
    sql = "select id from s_medicine.t_medicine_union where name =\'" + row[0] + "\'"
    ids = select(sql)
    for id in ids:
      txt = 'INSERT INTO "s_medicine"."t_manual"("medicine_name","ingredient", "indication", "dosage", "adverse_reaction", "contraindication", "consideration", "special_crowd", "drug_interaction", "pharmaco", "maximum","medicine_id" ) VALUES('
      for r in row:
        txt += '\'' + r.replace(' ','').replace('\n','').replace('\r','') + '\','
      txt += '\'' + str(id[0]) + '\','
      txts = txt[:-1] + ');\n'
      print (txts);
      write_txt(txts)
    # txt='INSERT INTO "s_mas"."t_box_info"("iccid","imei","mac","box_type","gsm_ver","bt_ver","bond_status","retry_times","mcu_ver") VALUES ('
    # if row[8]!=1001:
    #   if row[9] not in list:
    #     list.append(row[9])
    #     txt += '\'' + str(row[8]) + '\','
    #     txt += '\'' + str(int(row[9])) + '\','
    #     txt += '\'' + str(row[10]) + '\','
    #     txt += '\'' + '1' + '\','
    #     txt += '\'' + '0.2.4' + '\','
    #     txt += '\'' + 'BT' + '\','
    #     txt += '\'' + 'UNBOND' + '\','
    #     txt += '\'' + '0' + '\','
    #     txt += '\'' + '0.0.2' + '\','
    #     txts = txt[:-1] + ');\n'
    #     write_txt(txts)
    # insert(txts)
  # return list

def clean():
  with open("manual.txt", 'w') as f:
    f.write("")


def write_txt(txt):
  with open("manual.txt", 'a') as f:
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
