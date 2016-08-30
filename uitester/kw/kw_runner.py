import logging
import traceback
from .kw import KWCore


logger = logging.getLogger('Runner')


class StatusMsg:
    TEST_START = 1
    TEST_END = 2
    CASE_START = 101
    CASE_END = 102
    KW_LINE_START = 201
    KW_LINE_END = 202
    ERROR = 500

    status = None
    case_id = 0
    line_number = 0
    message = None

    __status_str__ = {
        TEST_START: 'TEST START',
        TEST_END: 'TEST END',
        CASE_START: 'CASE START',
        CASE_END: 'CASE END',
        KW_LINE_START: 'KW LINE START',
        KW_LINE_END: 'KW LINE END',
        ERROR: 'ERROR'
    }

    def __init__(self, status, case_id=0, line_number=0, message=None):
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


class DefaultKWRunningStatusListener(KWRunningStatusListener):

    def update(self, msg):
        logger.debug(str(msg))


class KWCase:
    id = None
    name = None
    tags = None
    content = None


class KWRunner:

    def __init__(self):
        self.running_status_listeners = []

    def run(self, kw_cases):
        self.__update_status(StatusMsg(StatusMsg.TEST_START))
        for kw_case in kw_cases:
            self.__update_status(StatusMsg(StatusMsg.CASE_START, case_id=kw_case.id))
            try:
                self.run_case(kw_case)
            except Exception as e:
                line_num = 0
                if len(e.args) >= 2:
                    line_num = e.args[1]
                error_msg = traceback.format_exc()
                self.__update_status(StatusMsg(
                    StatusMsg.ERROR,
                    case_id=kw_case.id,
                    line_number=line_num,
                    message=error_msg))
            self.__update_status(StatusMsg(StatusMsg.CASE_END, case_id=kw_case.id))
        self.__update_status(StatusMsg(StatusMsg.TEST_END))

    def run_case(self, kw_case):
        core = KWCore()
        for line in kw_case.content.split('\n'):
            core.parse_line(line.strip())
        core.execute()

    def __update_status(self, msg):
        for listener in self.running_status_listeners:
            listener.update(msg)
