# @Time    : 2016/10/24 11:30
# @Author  : lixintong
import os
from PyQt5 import uic

from PyQt5.QtWidgets import QWidget


class SettingWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_setting.ui')
        uic.loadUi(ui_file_path, self)
