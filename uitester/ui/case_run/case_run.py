# -*- encoding: UTF-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget

from uitester.config import Config
from uitester.ui.case_run.add_case import AddCaseWidget
from uitester.ui.case_run.add_device import AddDeviceWidget

device = None
cases = []


class RunWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_run.ui')
        uic.loadUi(ui_file_path, self)

        # set icon
        run_icon = QIcon()
        config = Config()
        run_icon.addPixmap(QPixmap(config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.runbtn.setIcon(run_icon)

        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.addbtn.setIcon(add_icon)

        self.addbtn.clicked.connect(self.click_add_case)
        self.runbtn.clicked.connect(self.click_run)

        self.add_case_widget = AddCaseWidget()
        self.add_device_widget = AddDeviceWidget()

    def click_add_case(self):
        self.add_case_widget.setWindowModality(Qt.ApplicationModal)  # 设置QWidget为模态
        self.add_case_widget.show()

    def click_run(self):
        self.add_device_widget.setWindowModality(Qt.ApplicationModal)
        self.add_device_widget.show()
