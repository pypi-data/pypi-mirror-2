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

import os.path as osp
from openpyxl.tests.helper import BaseTestCase, TMPDIR, DATADIR

from openpyxl.workbook import Workbook
from openpyxl.writer.excel import ExcelWriter

from openpyxl.writer.workbook import write_workbook, write_workbook_rels
from openpyxl.writer.worksheet import write_worksheet
from openpyxl.writer.strings import write_string_table

class TestWriter(BaseTestCase):

    def test_write_empty_workbook(self):

        wb = Workbook()

        ew = ExcelWriter(workbook = wb)

        dest_filename = osp.join(TMPDIR, 'empty_book.xlsx')

        ew.save(filename = dest_filename)

        self.assertTrue(osp.isfile(dest_filename))

class TestWriteWorkbook(BaseTestCase):

    def test_write_workbook_rels(self):

        wb = Workbook()

        content = write_workbook_rels(workbook = wb)

        self.assertEqualsFileContent(reference_file = osp.join(DATADIR, 'writer', 'expected', 'workbook.xml.rels'),
                                     fixture = content)

    def test_write_workbook(self):

        wb = Workbook()

        content = write_workbook(workbook = wb)

        self.assertEqualsFileContent(reference_file = osp.join(DATADIR, 'writer', 'expected', 'workbook.xml'),
                                     fixture = content)

class TestWriteStrings(BaseTestCase):

    def test_write_string_table(self):

        table = {'hello' : 1,
                 'world' : 2,
                 'nice' : 3}

        content = write_string_table(string_table = table)

        self.assertEqualsFileContent(reference_file = osp.join(DATADIR, 'writer', 'expected', 'sharedStrings.xml'),
                                     fixture = content)

class TestWriteWorksheet(BaseTestCase):

    def test_write_worksheet(self):

        wb = Workbook()

        ws = wb.create_sheet()

        ws.cell('F42').value = 'hello'

        content = write_worksheet(worksheet = ws, string_table = {'hello' : 0}, style_table = {})

        self.assertEqualsFileContent(reference_file = osp.join(DATADIR, 'writer', 'expected', 'sheet1.xml'),
                                     fixture = content)


    def test_write_worksheet_with_formula(self):

        wb = Workbook()

        ws = wb.create_sheet()

        ws.cell('F1').value = 10
        ws.cell('F2').value = 32
        ws.cell('F3').value = '=F1+F2'

        content = write_worksheet(worksheet = ws, string_table = { }, style_table = {})

        self.assertEqualsFileContent(reference_file = osp.join(DATADIR, 'writer', 'expected', 'sheet1_formula.xml'),
                                     fixture = content)
