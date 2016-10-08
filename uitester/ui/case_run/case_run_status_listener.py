import logging

from PyQt5.QtCore import pyqtSignal, QObject

from uitester.test_manager.kw_runner import KWRunningStatusListener

logger = logging.getLogger("Tester")


class CaseRunStatusListener(KWRunningStatusListener, QObject):
    listener_msg_signal = pyqtSignal(object, name="listener_msg_signal")

    def __init__(self):
        super().__init__()

    def update(self, msg):
        if msg.status == 101 or msg.status == 500 or msg.status == 2:
            logger.debug("case status: " + str(msg.status))
            self.listener_msg_signal.emit(msg)  # update case's color
