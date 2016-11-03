import logging

from PyQt5.QtCore import pyqtSignal, QObject

from uitester.test_manager.kw_runner import KWRunningStatusListener

logger = logging.getLogger("Tester")


class EditorRunStatusListener(KWRunningStatusListener, QObject):
    editor_listener_msg_signal = pyqtSignal(object, bool, name="editor_listener_msg_signal")

    def __init__(self):
        super().__init__()
        self.status_list = []  # all status

    def update(self, msg):
        if msg.status == 101:   # init data
            self.status_list.clear()
        self.status_list.append(msg.status)
        if msg.status == 500:
            logger.debug("case status update: " + str(msg.status) + ", error info:" + str(msg.message))
            self.editor_listener_msg_signal.emit(msg, False)  # fail
        elif msg.status == 102 and 500 not in self.status_list:
            self.editor_listener_msg_signal.emit(msg, True)  # pass
        elif msg.status == 102 and 500 in self.status_list:
            self.editor_listener_msg_signal.emit(msg, False)  # fail
        elif msg.status in (601, 602, 603, 701, 702, 703):  # install/agent status
            self.editor_listener_msg_signal.emit(msg, True)

