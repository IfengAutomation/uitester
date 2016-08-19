# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from uitester.config import Config


class AddCaseWidget(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_case.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        # set icon
        search_icon = QIcon()
        config = Config()
        search_icon.addPixmap(QPixmap(config.images + '/search.png'), QIcon.Normal, QIcon.Off)
        self.searchbtn.setIcon(search_icon)

        self.searchbtn.clicked.connect(self.search_event)
        self.selectcasebtn.clicked.connect(self.select_event)
        self.selectcasebtn.clicked.connect(self.hide)    # 隐藏AddCase页
        self.close_signal.connect(self.close)
        self.casecancelbtn.clicked.connect(self.cancel_event)

    def search_event(self):
        # TODO 1、获取搜索框tag_lineedit text，根据text进行数据查询
        # TODO 2、将结果以复选框形式显示在cases_to_choose
        pass

    def select_event(self):
        # TODO 记录选择数据，返回run主页
        pass

    def cancel_event(self):
        self.close()
