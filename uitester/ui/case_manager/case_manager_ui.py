# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtWidgets import *

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.tag_names_line_edit import TagCompleter, TagLineEdit


class CaseManagerUi(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_manager.ui')
        uic.loadUi(ui_file_path, self)
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit")
        self.query_conditions_layout.insertWidget(3, self.tag_names_line_edit)
        self.tag_list = self.dBCommandLineHelper.query_tag_all()
        self.set_tag_list_widget()
        self.set_tag_search_line()
        self.set_data_table_widget('点播')

    '''设置tag listWidget数据及触发事件
    '''

    def set_tag_list_widget(self):
        self.tag_list_widget.setFixedWidth(150)
        # self.tag_list_widget.setSelectionMode(QAbstractItemView::ExtendedSelection)  单选、多选
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
        # todo 设置 completer activated connect

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
        # todo 查询数据 、更换table 数据内容
        # def start():
        #     app = QApplication(sys.argv)
        #
        #     widget.show()
        #     sys.exit(app.exec_())

    '''
    设置tag text 内容
    '''

    def set_text_edit(self):
        pass

    '''
        设置动态数据表格
    '''

    def set_data_table_widget(self, tag_names):
        # todo tag_names 根据‘;’分割
        # todo 表格数据动态插入
        # todo 表格向下滑动时是否可动态加载  若不可以 什么容器可以 list？   分页操作
        # todo 数据导出时

        # todo 数据动态插入  时间倒序
        self.table_widget.setRowCount(30)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['名称', '最后修改时间', '标识', '操作'])
        tag_name_list = tag_names.split(';')
        row = 0
        for tag_name in tag_name_list:  # todo 修改逻辑 与操作
            case_data_list = self.dBCommandLineHelper.query_case_by_tag_name(tag_name)
            if len(case_data_list) > 0:
                for case in case_data_list:
                    self.table_widget.setItem(row, 0, QTableWidgetItem(case.name))
                    self.table_widget.setItem(row, 1, QTableWidgetItem(str(case.last_modify_time)))
                    tag_names = ""
                    for tag in case.tags:
                        tag_names = tag_names + tag.name + ","
                    self.table_widget.setItem(row, 2, QTableWidgetItem(tag_names[0:len(tag_names) - 1]))
                    row = row + 1
