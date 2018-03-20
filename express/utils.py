#!/bin/env python
# coding:utf8

import xlrd


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
            yield row_datas


def encode_gb2312(string):
    if isinstance(string, unicode):
        return string.encode('gb2312', 'ignore')
    else:
        return string


def data_iter(queryset):
    for data in queryset:
        start_time = str(data.start_time).split('.')[0]
        if data.end_time:
            end_time = str(data.end_time).split('.')[0]
        else:
            end_time = ''
        if data.detail_time:
            detail_time = str(data.detail_time).split('.')[0]
        else:
            detail_time = ''
        if data.progess_time:
            progess_time = str(data.progess_time).split('.')[0]
        else:
            progess_time = ''
        number = str(data.number).split('.')[0]
        datas = map(
            encode_gb2312,
            [
                number, data.orig, start_time, data.status, data.detail,
                detail_time, data.error_type, data.progess, progess_time,
                data.follower.first_name, data.resaon, end_time
            ]
        )
        yield datas
