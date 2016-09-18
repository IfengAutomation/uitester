from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from uitester.kw.kw_runner import KWRunningStatusListener


class CaseRunStatusListener(KWRunningStatusListener, QWidget):
    listener_msg_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def update(self, msg):
        if msg.status == 500 or msg.status == 102:
            self.listener_msg_signal.emit(msg.case_id, msg.status)  # update case's color
