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

from openpyxl.tests.helper import BaseTestCase

from openpyxl.workbook import Workbook
from openpyxl.worksheet import Worksheet
from openpyxl.cell import Cell

class TestWorksheet(BaseTestCase):

    def setUp(self):

        self.wb = Workbook()

    def test_new_worksheet(self):

        ws = Worksheet(parent_workbook = self.wb)

        self.assertEqual(self.wb, ws._parent)

    def test_get_cell(self):

        ws = Worksheet(parent_workbook = self.wb)

        c = ws.cell(coordinate = 'A1')

        self.assertEqual(c.get_coordinate(), 'A1')

    def test_set_wrong_title(self):

        self.assertRaises(Exception, Worksheet, self.wb, 'X' * 50)

    def test_worksheet_dimension(self):

        ws = Worksheet(parent_workbook = self.wb)

        self.assertEqual('A1:A1', ws.calculate_dimension())

        ws.cell('B12').value = 'AAA'

        self.assertEqual('A1:B12', ws.calculate_dimension())

    def test_worksheet_range(self):

        ws = Worksheet(parent_workbook = self.wb)

        rng = ws.range('A1:C4')

        self.assertTrue(isinstance(rng, tuple))

        self.assertEqual(4, len(rng))

        self.assertEqual(3, len(rng[0]))

    def test_worksheet_range_named_range(self):

        ws = Worksheet(parent_workbook = self.wb)

        self.wb.create_named_range(name = 'test_range', worksheet = ws, range = 'C5')

        rng = ws.range("test_range")

        self.assertTrue(isinstance(rng, Cell))

        self.assertEqual(5, rng.row) #pylint: disable-msg=E1103


