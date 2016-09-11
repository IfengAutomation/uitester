# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter, SearchButton
from uitester.ui.case_run.table_widget import RunnerTableWidget


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
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.search_button)
        self.tag_names_line_edit_adapter()   # 设置自动提示
        self.tag_list = None

        self.result_widget = RunnerTableWidget(self.dBCommandLineHelper.query_case_all(), [])
        self.result_table_layout.insertWidget(0, self.result_widget)

        self.message_box = QMessageBox()

        self.search_button.clicked.connect(self.search_event)
        self.selectcasebtn.clicked.connect(self.select_event)
        self.casecancelbtn.clicked.connect(self.close)

    def search_event(self):
        """
        获取搜索框tag_lineedit text，根据text进行数据查询
        结果以复选框形式显示
        :return:
        """
        self.result_widget.setParent(None)
        self.result_table_layout.removeWidget(self.result_widget)
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        case_list = []
        if tag_names != '':
            tag_names = tag_names[:len(tag_names)].split(';')
            case_list = self.dBCommandLineHelper.query_case_by_tag_names(tag_names)
        else:
            case_list = self.db_helper.query_case_all()
        self.result_widget = RunnerTableWidget(case_list, [])
        self.result_table_layout.insertWidget(0, self.result_widget)

    def select_event(self):
        """
        记录选择数据，返回run主页
        根据选择结果获得case id
        :return:
        """
        self.result_widget.get_checked_data()
        if not self.result_widget.checked_cases_message:
            self.message_box.warning(self, "Message", "Please choose cases first.", QMessageBox.Ok)
            return
        id_list = []
        for item in self.result_widget.checked_cases_message:
            id_list.append(int(item["case_id"]))
        self.select_case_signal.emit(id_list)
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
