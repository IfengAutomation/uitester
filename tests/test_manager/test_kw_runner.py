import unittest
from uitester.test_manager import kw_runner
import time

class Msg:
    pass


class Agent:
    def __init__(self):
        self.finish = False
        self.error = False
        self.e = None
        self.device_id = 'ABCD'
        self.expect = [
            {
                'method': 'GetView',
                'args': ['yyy-1'],
                'res': {
                    'msg_type': 2,
                    'msg_id': 1,
                    'name': 'response',
                    'args': [
                        {'id': 'yyy-1', 'clazz': 'TextView', 'text': 'Hello', 'hash': 123456}
                    ]
                }
            },
            {
                'method': 'ClickOnView',
                'args': [123456],
                'res': {
                    'msg_type': 2,
                    'msg_id': 1,
                    'name': 'response',
                    'args': [
                        True
                    ]
                }
            }
        ]

    def call(self, method, *args):
        try:
            res = self.expect.pop(0)
            if res['method'] is not method:
                raise AssertionError('Method not match expect {} but actual {}'.format(res['method'], method))
            if res['args'][0] != args[0]:
                raise AssertionError('Args not match expect {} but actual {}'.format(res['args'], args))
            msg = Msg()
            msg.__dict__ = res['res']
        except Exception as e:
            self.error = True
            self.e = e
            raise e
        if len(self.expect) == 0:
            self.finish = True
        return msg


class StatusListener:
    expect = [
        [101, 'ABCD', 0],
        [201, 'ABCD', 1],
        [202, 'ABCD', 1],
        [201, 'ABCD', 2],
        [202, 'ABCD', 2],
        [201, 'ABCD', 3],
        [202, 'ABCD', 3],
        [102, 'ABCD', 0],
    ]

    def __init__(self):
        self.finish = False
        self.error = False
        self.e = None

    def update(self, msg):
        try:
            expect_msg = self.expect.pop(0)
            assert expect_msg[0] == msg.status, 'expect {} actual {}'.format(expect_msg[0], msg.status)
            assert expect_msg[1] == msg.device_id
            assert expect_msg[2] == msg.line_number, 'expect {} actual {}'.format(expect_msg[2], msg.line_number)
            if msg.status == 500:
                assert msg.message
        except Exception as e:
            self.error = True
            self.e = e
            raise e
        if len(self.expect) == 0:
            self.finish = True


class KWRunnerTest(unittest.TestCase):

    def test_kw_core(self):
        agent = Agent()
        listener = StatusListener()
        script = 'import example\ngetView yyy-1 as v\nclickOnView $v'
        core = kw_runner.KWCore()
        core.parse(script)
        core.execute(agent, listener)

        time_count = 0
        while True:
            if time_count >= 5:
                raise TimeoutError('agent expect count {} . listener expect count {}'.format(len(agent.expect), len(listener.expect)))
            if agent.finish and listener.finish:
                break
            if agent.error:
                raise agent.e
            if listener.error:
                raise listener.e
            time.sleep(0.5)
            time_count += 0.5

