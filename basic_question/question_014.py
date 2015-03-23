#!/usr/bin/python

import os, xlrd, xlwt

if __name__ == '__main__':
    values = {
      '1': ['zhangsan', 150, 120, 100],
      '2': ['lisi'    , 90,  99,  95],
      '3': ['wangwu'  , 60,  66,  68]
      }
    wb = xlwt.Workbook()
    sheet = wb.add_sheet('sheet1')
    for i, x in values.iteritems():
        row = sheet.row(int(i)-1)
        row.write(0, i)
        for j,v in enumerate(x):
            row.write(j+1, v)
    wb.save('output_014.xlsx')
