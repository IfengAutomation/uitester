import unittest
from uitester.test_manager import tester


class TesterTest(unittest.TestCase):

    def test_debug(self):
        t = tester.Tester()
        _debug = t.get_debug_runner()
        _debug.parse('import example')
