# coding=UTF-8
'''
Copyright (c) 2010 openpyxl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

@license: http://www.opensource.org/licenses/mit-license.php
@author: Eric Gazoni
'''
from __future__ import with_statement
import os.path as osp
from shutil import copy
from openpyxl.tests.helper import BaseTestCase, TMPDIR, DATADIR

from openpyxl.worksheet import Worksheet
from openpyxl.workbook import Workbook

from openpyxl.style import NumberFormat, Style

from openpyxl.reader.worksheet import read_worksheet

from openpyxl.reader.excel import load_workbook

class TestReadWorksheet(BaseTestCase):

    def test_read_worksheet(self):

        class DummyWb(object):

            def get_sheet_by_name(self, value):

                return None

        with open(osp.join(DATADIR, 'reader', 'sheet2.xml')) as f:
            content = f.read()

            ws = read_worksheet(xml_source = content,
                                parent = DummyWb(),
                                preset_title = 'Sheet 2',
                                string_table = {1 : 'hello'},
                                style_table = {1 : Style()})

            self.assertTrue(isinstance(ws, Worksheet))

            self.assertEqual(ws.cell('G5').value, 'hello')

            self.assertEqual(ws.cell('D30').value, 30)

            self.assertEqual(ws.cell('K9').value, 0.09)

class TestReadWorkbook(BaseTestCase):

    def setUp(self):

        self.genuine_wb = osp.join(DATADIR, 'genuine', 'empty.xlsx')
        self.test_wb = osp.join(TMPDIR, 'test.xlsx')

        copy(self.genuine_wb, self.test_wb)

    def test_read_workbook(self):

        wb = load_workbook(filename = self.test_wb)

        self.assertTrue(isinstance(wb, Workbook))

    def test_read_worksheet(self):

        wb = load_workbook(filename = self.test_wb)

        sheet2 = wb.get_sheet_by_name(name = 'Sheet2 - Numbers')

        self.assertTrue(isinstance(sheet2, Worksheet))

        self.assertEqual('This is cell G5', sheet2.cell('G5').value)

        self.assertEqual(18, sheet2.cell('D18').value)


class TestReadWorkbookNoStringTable(BaseTestCase):

    def setUp(self):

        self.genuine_wb = osp.join(DATADIR, 'genuine', 'empty-no-string.xlsx')

    def test_read_workbook(self):

        wb = load_workbook(filename = self.genuine_wb)

        self.assertTrue(isinstance(wb, Workbook))

class TestReadWorkbookWithStyles(BaseTestCase):

    def setUp(self):

        self.genuine_wb = osp.join(DATADIR, 'genuine', 'empty-with-styles.xlsx')
        wb = load_workbook(filename = self.genuine_wb)
        self.ws = wb.get_sheet_by_name(name = 'Sheet1')

    def test_read_general_style(self):

        self.assertEqual(self.ws.cell('A1').style.number_format.format_code, NumberFormat.FORMAT_GENERAL)

    def test_read_date_style(self):

        self.assertEqual(self.ws.cell('A2').style.number_format.format_code, NumberFormat.FORMAT_DATE_XLSX14)

    def test_read_number_style(self):

        self.assertEqual(self.ws.cell('A3').style.number_format.format_code, NumberFormat.FORMAT_NUMBER_00)

    def test_read_time_style(self):

        self.assertEqual(self.ws.cell('A4').style.number_format.format_code, NumberFormat.FORMAT_DATE_TIME3)

    def test_read_percentage_style(self):

        self.assertEqual(self.ws.cell('A5').style.number_format.format_code, NumberFormat.FORMAT_PERCENTAGE_00)
