import unittest
from uitester.tester import Tester


class KWCase:
    id = None
    name = None
    tags = None
    content = None


class TesterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_run(self):
        tester = Tester()
        kw_case = KWCase()
        kw_case.id = 1
        kw_case.name = 'TestCase-1'
        kw_case.content = 'import example_lib\ntest_str\nget_view abcd\n'
        tester.run([kw_case])

