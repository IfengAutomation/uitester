from PyQt5.QtCore import pyqtSignal, QObject

from uitester.kw.kw_runner import KWRunningStatusListener


class CaseRunStatusListener(KWRunningStatusListener, QObject):
    listener_msg_signal = pyqtSignal(object, name="listener_msg_signal")

    def __init__(self):
        super().__init__()

    def update(self, msg):
        if msg.status == 101 or msg.status == 500 or msg.status == 2:
            self.listener_msg_signal.emit(msg)  # update case's color
