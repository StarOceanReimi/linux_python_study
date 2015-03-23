#!/usr/bin/python

import os, xlrd
from lxml import etree
from cStringIO import StringIO

if __name__ == '__main__':
    wb = xlrd.open_workbook('output_014.xlsx')
    sheet = wb.sheet_by_index(0)
    values = {}
    for row in range(sheet.nrows):
        values[str(row+1)] = []
        for col in range(sheet.ncols):
            values[str(row+1)].append(sheet.cell(row, col).value)

    info = '\n    {\n    '+"\n    ".join(["  '%s' : %s" % (k, ', '.join([str(x) for i,x in enumerate(v) if i!=0])) for k, v in values.iteritems()])+'\n    }\n'

    root = etree.Element('root')
    student = etree.SubElement(root, 'student')
    comment = etree.Comment()
    comment.text = '''
        student info:
        'id' : [name, math, verbal, english]
    '''
    student.insert(0, comment)
    comment.tail = info
    print etree.tostring(root, encoding='utf-8', xml_declaration=True, pretty_print=True)
