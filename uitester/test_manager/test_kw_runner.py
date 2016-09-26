from test_manager import kw_runner


def test_kw_core():
    core = kw_runner.KWCore()
    script = 'import example\ngetView yyy-1 as v\nclickOnView yyy-1'
    core.parse(script)
    core.execute(Agent())


class Agent:

    def call(self, method, *args):
        print('TEST agent call')
        return True


if __name__ == '__main__':
    test_kw_core()
