# -*- encoding: UTF-8 -*-
import sys
from PyQt5.QtWidgets import QRadioButton, QApplication,QMainWindow

from uitester.ui.case_run import case_run


class DeviceRadio(QRadioButton):
    def __init__(self, device_id, parent=None):
        super(DeviceRadio, self).__init__(parent)
        self.setObjectName(device_id)
        self.setText(device_id)
        self.clicked.connect(self.checked_event)

    def checked_event(self):
        """
        radio 被选中时处理数据
        :return:
        """
        if self.isChecked():
            device_id = self.text()
            case_run.device = device_id

if __name__ == '__main__':
    app = QApplication(sys.argv)
    radio = DeviceRadio("1111")

    window = QMainWindow()

    window.setCentralWidget(radio)
    window.show()
    app.exec_()
