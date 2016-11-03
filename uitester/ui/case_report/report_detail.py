# @Time    : 2016/11/3 10:32
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea


class ReportDetailWidget(QWidget):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'report_detail.ui')
        uic.loadUi(ui_file_path, self)
        self.message = eval(message)
        scroll_area = QScrollArea()
        message_label = QLabel()
        # message_label.setWordWrap(True)
        message_label_text = ''
        for key, value in self.message.items():
            message_label_text += "{} :\n{}\n".format(key, value)
        message_label.setText(message_label_text)
        scroll_area.setWidget(message_label)
        self.main_layout.addWidget(scroll_area)