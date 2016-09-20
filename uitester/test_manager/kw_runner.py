import threading
import time
import sys
from os.path import dirname, abspath, pardir, join
from uitester.test_manager import device_proxy


script_dir = dirname(abspath(__file__))
libs_dir = join(join(join(script_dir, pardir), pardir), 'libs')
sys.path.append(libs_dir)


class KWRunner:

    def execute(self):
        pass

    def task_handler(self, cases, agent):
        pass


class KWCore:

    def __init__(self):
        self.kw_func = {}

    def parse_line(self, line):
        pass

    def execute(self):
        pass

    def _import(self, module_name):
        m = __import__(module_name)
        if hasattr(m, 'var_cache'):
            m.var_cache['proxy'] = device_proxy
        self.kw_func.update(m.kw_func)

    def _execute(self):
        pass


class Agent:

    def call(self, method, *args):
        print('TEST agent call')
        return True


if __name__ == '__main__':
    core = KWCore()
    core._import('example')
    print(core.kw_func)
    from uitester.test_manager import context
    context.agent = Agent()
    core.kw_func['hello']()

