import unittest
from uitester.kw.kw import KWCore, KWLine
from uitester.context import Context


class TestKW(unittest.TestCase):
    def setUp(self):
        self._kw = KWCore(Context())

    def test_parse_line(self):
        kw_str = 'import example_lib'
        kw_line = self._kw._parse_line(kw_str, line_number=1)
        self.assertTrue(kw_line.raw == 'import example_lib')
        self.assertTrue(kw_line.comment is False)
        self.assertTrue(kw_line.line_number == 1)
        self.assertTrue(kw_line.items[0] == 'import')
        self.assertTrue(kw_line.items[1] == 'example_lib')

    def test_parse_line_error(self):
        kw_str = 'abc abc'
        try:
            kw_line = self._kw.parse_line(kw_str)
        except ValueError as e:
            self.assertEqual('Define not found abc', e.args[0])

    def test_parse_kw_as(self):
        kw_str_1 = 'import kw_proxy'
        kw_str_2 = 'get_view id as v'

        self._kw.parse_line(kw_str_1)
        self._kw.parse_line(kw_str_2)

    def test_import_error(self):
        kw_1 = 'import not_found_lib'

        try:
            self._kw.parse_line(kw_1)
        except ImportError as e:
            self.assertEqual('No module named \'not_found_lib\'', e.args[0])

    def test_execute(self):
        kw_list = ['import kw_proxy',
                   'import example_lib',
                   'test_str as s',
                   'print s']
        for kw in kw_list:
            self._kw.parse_line(kw)
        self._kw.execute()

