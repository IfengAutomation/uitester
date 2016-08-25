# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_edit import CaseEdit
from uitester.ui.case_manager.table_layout import TableLayout
from uitester.ui.case_manager.tag_names_line_edit import TagCompleter, TagLineEdit


class CaseManagerUi(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_manager.ui')
        uic.loadUi(ui_file_path, self)
        self.query_cases_button.clicked.connect(self.update_table_data)  # tag names 查询
        self.add_case_button.clicked.connect(self.add_case)# 添加case 事件
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit")
        self.query_conditions_layout.insertWidget(3, self.tag_names_line_edit)  # 插入查询输入框
        self.tag_list = self.dBCommandLineHelper.query_tag_all()
        self.set_tag_list_widget()  # 显示所有标签
        self.set_tag_search_line()  # 设置输入框自动补全
        self.table_layout = TableLayout('')  # 显示数据表及相应操作
        self.data_message_layout.insertWidget(1, self.table_layout)

    def add_case(self):
        self.add_case_window = CaseEdit(case_id=None)
        self.add_case_window.setWindowModality(Qt.ApplicationModal)  # 设置QWidget为模态
        self.add_case_window.show()
    '''根据查询条件更新数据表'''

    def update_table_data(self):
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        if tag_names != '':
            tag_names = tag_names[:len(tag_names)]
        self.table_layout.update_table_data(tag_names)

    '''设置tag listWidget数据及触发事件
    '''

    def set_tag_list_widget(self):
        self.tag_list_widget.setFixedWidth(150)
        for tag in self.tag_list:
            self.tag_list_widget.addItem(tag.name)
        self.tag_list_widget.itemClicked.connect(
            lambda: self.list_widget_item_clicked(self.tag_list_widget.currentItem()))

    '''
        设置tag 搜索栏
    '''

    def set_tag_search_line(self):
        tag_completer = TagCompleter(self.get_tag_names())
        self.tag_names_line_edit.setCompleter(tag_completer)

    def get_tag_names(self):
        tag_model_list = []
        for tag in self.tag_list:
            tag_model_list.append(tag.name)
        return tag_model_list

    def list_widget_item_clicked(self, tag_list_widget_item):
        self.tag_names_line_edit.clear()
        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.setText(tag_list_widget_item.text() + ";")
        self.tag_names_line_edit.is_completer = True
