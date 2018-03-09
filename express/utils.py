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
        for i in range(excel_sheet.nrows):
            yield excel_sheet.row_values(i)


def to_datetime(str_time):
    return datetime.strptime(str_time, '%Y/%m/%d %H:%M:%S')


def to_unicode(string):
    if isinstance(string, unicode):
        return string.encode('utf8')
    else:
        return string
