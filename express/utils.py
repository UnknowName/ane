#!/bin/env python
# coding:utf8

import xlrd
from datetime import datetime


def read_excel(file_contents):
    excel = xlrd.open_workbook(
        file_contents=file_contents,
        encoding_override='utf8'
    )
    for excel_sheet in excel.sheets():
        for row in xrange(excel_sheet.nrows):
            row_datas = list()
            for col in xrange(excel_sheet.ncols):
                data = excel_sheet.cell(row, col)
                if data.ctype == 3:
                    cell_data = xlrd.xldate_as_datetime(
                        data.value,
                        excel.datemode
                    )
                else:
                    if isinstance(data.value, unicode):
                       cell_data = data.value.encode('utf8')
                    else:
                        cell_data = data.value
                row_datas.append(cell_data)
            #print row_datas
            yield row_datas


def to_datetime(str_time):
    #print str_time
    try:
        return datetime.strptime(str_time, '%Y/%m/%d %H:%M:%S')
    except Exception:
        return datetime.strptime(str_time, '%Y/%m/%d %H:%M')
        

def encode_utf8(string):
    if isinstance(string, unicode):
        return string.encode('utf8')
    else:
        return string


def write_excel(filename, lst):
    row = 0
    excel = xlwt.Workbook(encoding='utf8')
    excel_sheet = excel.add_sheet('sheet1')
    for col, data in enumerate(lst):
        excel_sheet.write(row, col, data)
    row += 1
    excel.save(filename)


def file_iter(filename, chunk_size=512):
    with open(filename) as f:
        while True:
            content = f.read(chunk_size)
            if content:
                yield content
            else:
                break
