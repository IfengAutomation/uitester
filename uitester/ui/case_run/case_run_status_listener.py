import logging

from PyQt5.QtCore import pyqtSignal, QObject

from uitester.test_manager.kw_runner import KWRunningStatusListener

logger = logging.getLogger("Tester")


class CaseRunStatusListener(KWRunningStatusListener, QObject):
    listener_msg_signal = pyqtSignal(object, bool, name="listener_msg_signal")

    def __init__(self):
        super().__init__()
        self.status_list = []  # all status

    def update(self, msg):
        if msg.status == 1:  # init data
            self.status_list.clear()

        self.status_list.append(msg.status)  # append msg status
        if msg.status == 101:
            self.listener_msg_signal.emit(msg, True)
        elif msg.status == 500:
            logger.debug("case status: " + str(msg.status))
            self.listener_msg_signal.emit(msg, False)  # update case's color
        elif msg.status == 2 and 500 not in self.status_list:
            self.listener_msg_signal.emit(msg, True)  # pass
        elif msg.status == 2 and 500 in self.status_list:
            self.listener_msg_signal.emit(msg, False)  # fail
        elif msg.status in (601, 602, 603, 701, 702, 703):  # install/agent status
            self.listener_msg_signal.emit(msg, True)
