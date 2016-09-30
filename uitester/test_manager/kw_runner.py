import threading
import time
import sys
from os.path import dirname, abspath, pardir, join
from uitester.test_manager import device_proxy
import logging
from uitester.test_manager import context


logger = logging.getLogger('Tester')

script_dir = dirname(abspath(__file__))
libs_dir = join(join(join(script_dir, pardir), pardir), 'libs')
sys.path.append(libs_dir)


class StatusMsg:
    TEST_START = 1
    TEST_END = 2
    CASE_START = 101
    CASE_END = 102
    KW_LINE_START = 201
    KW_LINE_END = 202
    ERROR = 500

    __status_str__ = {
        TEST_START: 'TEST START',
        TEST_END: 'TEST END',
        CASE_START: 'CASE START',
        CASE_END: 'CASE END',
        KW_LINE_START: 'KW LINE START',
        KW_LINE_END: 'KW LINE END',
        ERROR: 'ERROR'
    }

    def __init__(self, status, device_id=None, case_id=0, line_number=0, message=None):
        self.device_id = device_id
        self.status = status
        self.case_id = case_id
        self.line_number = line_number
        self.message = message

    def __str__(self):
        message = self.message if self.message else ''
        return '{} case_id={} line_number={} message:\n {}'\
            .format(self.__status_str__[self.status], self.case_id, self.line_number, message)


class KWRunningStatusListener:
    """
    TestCase running status listener
    """
    def update(self, msg):
        """
        When test runner status changed. Runner will call function update
        :param msg :StatusMsg
        :return:
        """
        pass


class RunSignal:
    stop = False


class DataRow:

    @classmethod
    def from_row(cls, headers, data_row):
        data_dict = {}
        for index, header in enumerate(headers):
            data_dict[header] = data_row[index]
        data = cls()
        data.__dict__ = data_dict
        return data

    @classmethod
    def from_list(cls, headers, data_rows):
        rows = []
        for row in data_rows:
            rows.append(cls.from_row(headers, row))
        return rows


class KWRunner:
    def __init__(self, status_listener=None):
        self.listener = status_listener
        self.run_signal = RunSignal()

    def execute(self, cases, agents):
        self.run_signal.stop = False
        for agent in agents:
            t = threading.Thread(target=self._run_cases_on_agent, args=(cases, agent))
            t.start()

    def _run_cases_on_agent(self, cases, agent):
        self.listener.update(StatusMsg(
                    StatusMsg.TEST_START,
                    device_id=agent.device_id
                ))
        context.agent = agent
        for _case in cases:
            core = KWCore()
            core.case_id = _case.id
            if len(_case.data) >= 2:
                data_rows = DataRow.from_list(_case.data[0], _case.data[1:])
                for data_row in data_rows:
                    core.reset()
                    core.set_data(data_row)
                    core.parse(_case.content)
                    core.execute(agent, self.listener)
            else:
                core.parse(_case.content)
                core.execute(agent, self.listener)
        self.listener.update(StatusMsg(
            StatusMsg.TEST_END,
            device_id=agent.device_id
        ))

    def stop(self):
        self.run_signal.stop = True


class KWDebugRunner:
    def __init__(self, device_manager, data=None, status_listener=None):
        self.dm = device_manager
        self.listener = status_listener
        self.run_signal = RunSignal()
        self.core = KWCore(self.run_signal)
        self._data = data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data is None:
            return
        if len(data) < 2:
            raise ValueError('DebugRunner: Empty data list')
        self._data = DataRow.from_list(data[0], data[1:])

    def reset(self):
        self.core.reset()
        self._data = None
        self.run_signal.stop = False

    def parse(self, script_str):
        self.core.parse(script_str)

    def execute(self, script_str=None, data_line=0):
        t = threading.Thread(target=self._thread_execute, args=(script_str, data_line))
        t.start()

    def _thread_execute(self, script_str=None, data_line=0):
        if data_line == 0:
            if self.data is None or len(self.data) < 2:
                self._execute(script_str=script_str)
            else:
                for data_row in self.data[1:]:
                    self._execute(script_str=script_str, data_row=data_row)
        else:
            self._execute(script_str=script_str, data_row=self.data[data_line])

    def _execute(self, script_str=None, data_row=None):
        self.run_signal.stop = False
        if script_str:
            self.core.reset()
            self.core.set_data(data_row)
            self.core.parse(script_str)
        agent = self.dm.selected_devices[0].agent
        self.core.execute(agent, self.listener, thread=True)

    def stop(self):
        self.run_signal.stop = True

    def get_var(self, var_name):
        if var_name == '':
            return self.core.kw_var.keys()
        res = []
        for v_name in self.core.kw_var:
            if var_name in v_name:
                res.append(v_name)
        return res

    def get_func(self, func_name):
        if func_name == '':
            return self.core.kw_func
        res = {}
        for f_name in self.core.kw_func:
            if func_name in f_name:
                res[f_name] = self.core.kw_func[f_name]
        return res

    def get_property(self, var_name, property_name):
        var = self.core.kw_var.get(var_name)
        if not var:
            return ['id', 'class', 'text']
        return filter(lambda x: False if x.startswith('__') or property_name not in x else True, var.__dict__.keys())


class KWCore:
    AS = 'as'
    QUOTE = '"'
    SPACE = ' '
    COMMENT = '#'
    DOT = '.'
    VAR = '$'
    DATA = 'data'

    def __init__(self, run_signal=None):
        self.default_func = {'import': self._import, 'check': self._check}
        self.kw_func = {**self.default_func}
        self.kw_var = {}
        self.kw_lines = []
        self.status_listener = None
        self.line_count = 0
        self.case_id = 0
        self.run_signal = run_signal

    def reset(self):
        """
        reset core. clear all func\var\listener\line count.
        """
        self.kw_func = {**self.default_func}
        self.kw_var = {}
        self.kw_lines = []
        self.status_listener = None
        self.line_count = 0
        if self.run_signal:
            self.run_signal.stop = False

    def set_data(self, data_row):
        self.kw_var[self.DATA] = data_row

    def parse(self, script_str):
        """
        parse keywords script
        It will raise exceptions while parse fail
        """
        lines = script_str.split('\n')
        for line in lines:
            self.parse_line(line)

    def parse_line(self, line):
        """
        parse single keywords script line
        """
        # set line number
        self.line_count += 1
        if len(line) == 0:
            return

        # parse line to kw line
        kw_line = self._parse_line(line, line_number=self.line_count)
        if kw_line.is_comment:
            return

        func = kw_line.items[0]

        # pre import lib
        if func == 'import':
            self.default_func['import'](*kw_line.items[1:])

        if func not in self.kw_func and func not in self.kw_var:
            raise ValueError('Define not found {}'.format(func), kw_line.line_number)

        # set var
        if kw_line.var:
            self.kw_var[kw_line.var] = None

        # add kw line to cache
        self.kw_lines.append(kw_line)

    def execute(self, agent, listener, thread=False):
        if thread:
            threading.Thread(target=self._execute, args=(agent, listener)).start()
        else:
            self._execute(agent, listener)

    def _execute(self, agent, listener):
        self.status_listener = listener
        context.agent = agent
        # run all kw line in cache
        if self.status_listener:
            # -- Case start --
            self.status_listener.update(StatusMsg(
                StatusMsg.CASE_START,
                device_id=agent.device_id,
                case_id=self.case_id
            ))
        for line in self.kw_lines:
            if self.status_listener:
                # -- Line start --
                self.status_listener.update(StatusMsg(
                    StatusMsg.KW_LINE_START,
                    device_id=agent.device_id,
                    line_number=line.line_number,
                    case_id=self.case_id
                ))
            try:
                if self.run_signal and self.run_signal.stop:
                    logger.debug('KWCore._execute : User stop test')
                    break
                self._execute_line(line)
            except Exception as e:
                if self.status_listener:
                    # -- Error --
                    self.status_listener.update(StatusMsg(
                        StatusMsg.ERROR,
                        device_id=agent.device_id,
                        line_number=line.line_number,
                        case_id=self.case_id,
                        message=e
                    ))
            if self.status_listener:
                # -- Line end --
                self.status_listener.update(StatusMsg(
                    StatusMsg.KW_LINE_END,
                    device_id=agent.device_id,
                    line_number=line.line_number,
                    case_id=self.case_id
                ))
        if self.status_listener:
            # -- Case end --
            self.status_listener.update(StatusMsg(
                StatusMsg.CASE_END,
                device_id=agent.device_id,
                case_id=self.case_id
            ))

    def _import(self, module_name):
        """
        Import python lib from .libs dir
        After import, you can use functions in py lib by write function name.
        ------------
        e.g.:
        import example
        test_str
        ------------
        line 1. Import python lib witch named custom_lib in libs dir.
        line 2. call function test_str() in custom_lib.

        """
        m = __import__(module_name)
        if hasattr(m, 'var_cache'):
            m.var_cache['proxy'] = device_proxy
        self.kw_func.update(m.kw_func)

    def _check(self, expected, actual):
        """
        Assert if arg1 equals arg2
        e.g. :
        check some_view.text some_text
        if this view's text is not some_text, then this case will be record as failed
        """
        assert expected == actual, 'Assert fail. expected={} but actual={}'.format(expected, actual)

    def _execute_line(self, kw_line):
        if kw_line.is_comment:
            # comment line
            return
        elif kw_line.items[0] == 'import':
            # import has been executed while parse line
            return
        logger.debug('exec items {}'.format(kw_line.items))

        # make args, change var name to var object
        args = []
        for item in kw_line.items[1:]:
            if item.startswith(self.VAR):
                arg_str = item[1:]
                index = arg_str.find(self.DOT)
                if index == -1:
                    args.append(self.kw_var[arg_str])
                else:
                    var = self.kw_var[arg_str[:index]]
                    args.append(getattr(var, arg_str[index+1:]))
            else:
                args.append(item)

        # execute keyword function
        res = self.kw_func[kw_line.items[0]](*args)
        # set response as var
        if kw_line.var:
            self.kw_var[kw_line.var] = res

    def _parse_line(self, kw_line, line_number=0):
        line = KWLine(raw=kw_line, line_number=line_number)
        if kw_line.strip().startswith(self.COMMENT):
            line.is_comment = True
            return line

        kw_items = []
        cache = None
        in_quotation = False
        var = None
        for char in kw_line:
            if char == self.SPACE and not in_quotation and cache:
                kw_items.append(cache)
                cache = None
            elif char == self.QUOTE:
                in_quotation = not in_quotation
            else:
                if not cache:
                    cache = char
                else:
                    cache += char
        if cache:
            kw_items.append(cache)

        if in_quotation:
            raise ValueError('Missing quote. {}'.format(kw_line), line_number)

        if self.AS in kw_items:
            as_index = kw_items.index(self.AS)
            if as_index < (len(kw_items) - 2):
                raise ValueError('Keywords "as" should only set one variable', line_number)
            elif as_index == (len(kw_items) - 1):
                raise ValueError('Keywords "as" need one variable after it', line_number)
            else:
                var = kw_items[as_index + 1]
                kw_items = kw_items[:as_index]

        for item in kw_items:
            if item.startswith(self.VAR) and len(item) > 1 and item[1:] not in self.kw_var:
                raise ValueError('Var {} not defined'.format(item[1:]))

        line.items = kw_items
        line.var = var
        return line


class KWLine:
    def __init__(self, raw=None, line_number=0):
        self.is_comment = False
        self.items = []
        self.raw = raw
        self.line_number = line_number
        self.var = None

