# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import *

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_edit import CaseEdit
from uitester.ui.case_manager.table_layout import TableLayout
from uitester.ui.case_manager.case_search_edit import TagCompleter, TagLineEdit, SearchButton


class CaseManagerUi(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_helper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_manager.ui')
        uic.loadUi(ui_file_path, self)
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.add_case_button.clicked.connect(self.add_case)  # 添加case 事件
        # case 搜索
        self.search_button = SearchButton()
        self.search_button.clicked.connect(self.update_table_data)
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.search_button)
        self.query_conditions_layout.insertWidget(5, self.tag_names_line_edit)
        # 表格数据初始化
        case_list = self.db_helper.query_case_all()
        self.table_layout = TableLayout(case_list)  # 显示数据表及相应操作
        self.delete_case_button.clicked.connect(self.delete_case)
        self.check_button.clicked.connect(self.check_or_cancel_all)
        self.button_style( self.delete_case_button, '/delete.png', "Delete")
        self.button_style(self.add_case_button, '/add.png', "Add")
        self.button_style(self.import_button, '/import.png', "Import")
        self.button_style(self.export_button, '/export.png', "Export")
        self.button_style(self.check_button, '/check_all.png', "Check All")

        self.tag_list = self.db_helper.query_tag_all()
        self.set_tag_list_widget()  # 显示所有标签
        self.set_tag_search_line()  # 设置输入框自动补全
        self.data_message_layout.insertWidget(1, self.table_layout)


    def button_style(self,button,image_path,text):
        icon = QIcon()
        config = Config()
        icon.addPixmap(QPixmap(config.images + image_path), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setText(text)
        button.setStyleSheet(
            "QPushButton{border-width:0px; background:transparent;} ")

    def check_or_cancel_all(self):
        text = self.check_button.text()
        check_status = Qt.Checked
        if text == 'Check All':
            self.check_button.setText("Cancel Check")
        else:
            self.check_button.setText("Check All")
            check_status = Qt.Unchecked
        for row in range(0, self.table_layout.dataTableWidget.rowCount()):
            check_box_item = self.table_layout.dataTableWidget.item(row, 0)
            check_box_item.setCheckState(check_status)

    def delete_case(self):
        self.table_layout.get_checked_data()
        if len(self.table_layout.checked_cases_message) > 0:
            infor_message = "确认删除" + str(len(self.table_layout.checked_cases_message)) + "条case"
            reply = QMessageBox.information(self, "删除提示", infor_message, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                for i in range(0, len(self.table_layout.checked_cases_message)):
                    case_message = self.table_layout.checked_cases_message[i]
                    print(int(case_message['case_id']))
                    self.db_helper.delete_case(int(case_message['case_id']))
                    self.table_layout.dataTableWidget.removeRow(int(case_message['row_num']) - i)  # 删除行后 行数会变 所以-i
                del self.table_layout.checked_cases_message[:]  # todo statusbar 应该提示
        else:
            QMessageBox.warning(self, "删除错误", "请选择要删除的case")

    def add_case(self):
        self.add_case_window = CaseEdit(case_id=None)
        self.add_case_window.setWindowModality(Qt.ApplicationModal)  # 设置QWidget为模态
        self.add_case_window.show()

    '''根据查询条件更新数据表'''

    def update_table_data(self):
        self.table_layout.setParent(None)
        self.data_message_layout.removeWidget(self.table_layout)
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        case_list = []
        if tag_names != '':
            tag_names = tag_names[:len(tag_names)].split(';')
            case_list = self.db_helper.query_case_by_tag_names(tag_names)
        self.table_layout = TableLayout(case_list)
        self.data_message_layout.insertWidget(1, self.table_layout)

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
        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.clear()
        self.tag_names_line_edit.setText(tag_list_widget_item.text() + ";")
        self.update_table_data()
        self.tag_names_line_edit.is_completer = True
        self.button_style(self.check_button, '/check_all.png', "Check All")

