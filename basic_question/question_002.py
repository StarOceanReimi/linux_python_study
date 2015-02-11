#!/usr/bin/python

from warnings import filterwarnings
import MySQLdb as mc, question_001 as pcode_gen

filterwarnings('ignore', category=mc.Warning)

dbname = 'py_exec'
tblname = 'promotion'
dbconfig = dict(host='localhost', user='qiuli', passwd='860226')
def init_db(): 
  conn = mc.connect(**dbconfig)
  cursor = conn.cursor()
  cursor.execute("drop database if exists %s;" % dbname)
  cursor.execute("create database %s charset='utf8';" % dbname)
  cursor.close()
  conn.close()  
  print 'database %s has been created' % dbname

  dbconfig['db'] = dbname
  conn = mc.connect(**dbconfig)
  cursor = conn.cursor()
  cursor.execute('drop table if exists %s' % tblname)
  cursor.execute('''create table %s(
                    id  int auto_increment primary key, 
                    code varchar(50) not null,
                    remark varchar(50) not null)''' % \
                    tblname)
  cursor.close()
  conn.close()
  print 'table %s has been created' % tblname

def save_promo_code(remark):
  pcg = pcode_gen.PromoCodeGenerator(200, 20)
  codes = pcg.get_codes()
  codes_db = [(code, remark) for code in codes]
  conn = mc.connect(**dbconfig)
  cursor = conn.cursor()
  sql = 'insert into {0} values(NULL, %s, %s)'.format(tblname)
  cursor.executemany(sql, codes_db)
  conn.commit()  
  cursor.close()
  conn.close()
  print 'promotion code has saved'

if __name__ == '__main__':
  init_db()
  save_promo_code('for old cusomter 10% discount!')



