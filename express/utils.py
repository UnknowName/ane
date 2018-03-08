#!/bin/env python
# coding:utf8

import xlrd


def read_excel(file_name):
    excel = xlrd.open_workbook(filename, encoding_overrid='utf8')
    for excel_sheet in excel.sheets():
        for i in range(excel_sheet.nrows):
            yield excel_sheet.row_values(i)
