# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter, SearchButton


class AddCaseWidget(QWidget):
    select_case_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_case.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        # tag name 输入框
        self.search_button = SearchButton()
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit",self.search_button)
        self.tag_names_line_edit_adapter()   # 设置自动提示
        self.tag_list = None

        # set icon
        search_icon = QIcon()
        config = Config()
        search_icon.addPixmap(QPixmap(config.images + '/search.png'), QIcon.Normal, QIcon.Off)
        self.searchbtn.setIcon(search_icon)

        self.searchbtn.clicked.connect(self.search_event)
        self.selectcasebtn.clicked.connect(self.select_event)
        self.casecancelbtn.clicked.connect(self.close)

    def search_event(self):
        # TODO 1、获取搜索框tag_lineedit text，根据text进行数据查询
        # TODO 2、将结果以复选框形式显示在cases_to_choose
        pass

    def select_event(self):
        # TODO 记录选择数据，返回run主页
        # TODO 根据选择结果获得case id
        self.close()     # 关闭AddCase页

    def tag_names_line_edit_adapter(self):
        """
        给tag_names_line_edit设置自动提示、默认显示提示文字等
        :return:
        """
        self.tag_names_line_edit.setPlaceholderText("Tag names")   # 设置提示文字
        self.search_layout.insertWidget(0, self.tag_names_line_edit)

        self.tag_list = self.dBCommandLineHelper.query_tag_all()  # 获取所有tag
        tag_name_list = []
        for tag in self.tag_list:
            tag_name_list.append(tag.name)
        cmp = TagCompleter(tag_name_list)
        self.tag_names_line_edit.setCompleter(cmp)
