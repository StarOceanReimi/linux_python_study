#!/usr/bin/python

import os, xlrd, xml.dom.minidom
from xml.etree import ElementTree as ET
from cStringIO import StringIO

def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element

ET._original_serialize_xml = ET._serialize_xml
def _serialize_xml(write, elem, encoding, qnames, namespaces):
    if elem.tag == '![CDATA[':
        write('\n<%s%s]]>\n' % (elem.tag, elem.text.encode(encoding)))
        return
    return ET._original_serialize_xml(write, elem, encoding, qnames, namespaces)
ET._serialize_xml = ET._serialize['xml'] = _serialize_xml


def pretty_print(xml_str):
    doc = xml.dom.minidom.parseString(xml_str)
    return doc.toprettyxml(indent='  ')

if __name__ == '__main__':
    wb = xlrd.open_workbook('output_014.xlsx')
    sheet = wb.sheet_by_index(0)
    values = {}
    for row in range(sheet.nrows):
        values[str(row+1)] = []
        for col in range(sheet.ncols):
            values[str(row+1)].append(sheet.cell(row, col).value)

    info = '{\n    '+"\n    ".join(["  '%s' : %s" % (k, ', '.join([str(x) for i,x in enumerate(v) if i!=0])) for k, v in values.iteritems()])+'\n    }'
    tree = ET.ElementTree()
    root = ET.Element('root')
    student = ET.SubElement(root, 'student')
    tree._setroot(root)
    comment = ET.Comment()
    comment.text = '''
        student info:
        'id' : [name, math, verbal, english]
      '''
    student.append(comment)
    cdata = CDATA(info)
    student.append(cdata)
    xml_io = StringIO()
    tree.write(xml_io, encoding='utf-8', xml_declaration=True)
    print pretty_print(xml_io.getvalue())
