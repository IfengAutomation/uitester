import unittest
from uitester.kw.kw_runner import KWRunningStatusListener, KWCase, KWRunner, StatusMsg


class TestKWRunner(unittest.TestCase):

    def test_run(self):
        kw_case = KWCase()
        kw_case.id = 1
        kw_case.name = 'simple test'
        kw_case.content = 'import remote_proxy\nimport custom_lib\ntest_str as s\nprint w\nh h'

        runner = KWRunner()
        runner.running_status_listeners.append(TestStatusListener())
        runner.run([kw_case])


class TestStatusListener(KWRunningStatusListener):

    def __init__(self):
        super().__init__()
        self.status_cases = [
            StatusMsg.TEST_START,
            StatusMsg.CASE_START,
            StatusMsg.ERROR,
            StatusMsg.CASE_END,
            StatusMsg.TEST_END
        ]
        self.line_count_cases = [0, 0, 5, 0, 0]

    def update(self, msg):
        status = self.status_cases.pop(0)
        assert status == msg.status, 'status is {} expect {}'.format(msg.status, status)
        line_num = self.line_count_cases.pop(0)
        assert msg.line_number == line_num, 'line = {} expect {}'.format(msg.line_number, line_num)
