from PyQt5.QtCore import pyqtSignal, QObject

from uitester.test_manager.kw_runner import KWRunningStatusListener


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
            self.editor_listener_msg_signal.emit(msg, False)  # fail
        if msg.status == 102 and 500 not in self.status_list:
            print(self.status_list)
            self.editor_listener_msg_signal.emit(msg, True)  # pass

