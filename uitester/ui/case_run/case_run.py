# -*- encoding: UTF-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox


class RunWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_run.ui')
        uic.loadUi(ui_file_path, self)
        self.addbtn.clicked.connect(self.click_add_case)

    def click_add_case(self):
        # TODO 弹窗 add case
        QMessageBox.about(self, "test", "test massage")

