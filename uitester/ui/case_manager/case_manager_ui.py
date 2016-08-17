# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class CaseManagerUi(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_manager.ui')
        uic.loadUi(ui_file_path, self)
        self.pushButton.clicked.connect(self.print)
    def print(self):
        print("xxxxx")
        # def start():
        #     app = QApplication(sys.argv)
        #
        #     widget.show()
        #     sys.exit(app.exec_())
