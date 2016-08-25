# @Time    : 2016/8/22 13:46
# @Author  : lixintong
import math
import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_edit import CaseEdit


class TableLayout(QWidget):
    def __init__(self, tag_names, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'table_layout.ui')
        uic.loadUi(ui_file_path, self)
        self.db_helper = DBCommandLineHelper()  # todo table 中也有help 要不要合并
        self.delete_case_button.clicked.connect(self.delete_case)  # 删除
        self.dataTableWidget = DataTableWidget(tag_names)  # 根据查询条件获取table data
        self.table_layout.insertWidget(0, self.dataTableWidget)
        self.delete_cases_message = []  # 待删除Id
        self.set_page_data()  # 根据查询条件获取 分页 page 数据

    def update_table_data(self, tag_names):  # 1;2;3 格式
        tag_names_list = tag_names.split(';')
        self.dataTableWidget.set_table_data(tag_names_list)
        self.set_page_data()

    def get_checked_data(self):
        for row_num in range(0, self.dataTableWidget.rowCount()):
            checkbox_item = self.dataTableWidget.item(row_num, 0)
            if checkbox_item.checkState() == Qt.Checked:
                case_id = self.dataTableWidget.item(row_num, 1).text()
                self.delete_cases_message.append({"case_id": case_id, "row_num": row_num})

    def delete_case(self):
        self.get_checked_data()
        if len(self.delete_cases_message) > 0:
            infor_message = "确认删除" + str(len(self.delete_cases_message)) + "条case"
            reply = QMessageBox.information(self, "删除提示", infor_message, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                for i in range(0, len(self.delete_cases_message)):  # todo 批量删除时，发生部分删除 要做记录
                    self.db_helper.delete_case(self.delete_cases_message[i]['case_id'])
                    self.dataTableWidget.removeRow(self.delete_cases_message[i]['row_num'] - i)
                del self.delete_cases_message[:]  # todo statusbar 应该提示
        else:
            QMessageBox.warning(self, "删除错误", "请选择要删除的case")

    def set_page_data(self):
        self.page_label.setText("共" + str(len(self.dataTableWidget.case_list)) + "条case")


class DataTableWidget(QTableWidget):
    header_text_list = ['', 'id', '名称', '最后修改时间', '标识']
    column_count = len(header_text_list)

    def __init__(self, tag_names_list, *args):
        super().__init__(*args)
        self.setObjectName("data_table_widget")
        self.db_helper = DBCommandLineHelper()
        self.set_table_data(tag_names_list)

    def set_table_data(self, tag_names_list):
        if len(tag_names_list) > 0:
            self.case_list = self.db_helper.query_case_by_tag_names(tag_names_list)
        else:
            self.case_list = self.db_helper.query_case_all()
        self.setRowCount(len(self.case_list))
        self.setColumnCount(self.column_count)
        self.set_table_header()

        self.setColumnWidth(0, 40)
        self.setColumnWidth(2, 140)
        self.setColumnWidth(3, 140)  # todo 待修改
        self.resizeColumnToContents(0)

        self.itemClicked.connect(self.item_clicked)
        for row in range(0, self.rowCount()):
            self.set_checkbox_item(row, 0)
            case = self.case_list[row]
            self.setItem(row, 1, QTableWidgetItem(str(case.id)))
            self.setItem(row, 2, QTableWidgetItem(case.name))
            self.setItem(row, 3, QTableWidgetItem(case.last_modify_time.strftime("%Y-%m-%d %H:%M:%S")))
            tag_names = ''
            for tag in case.tags:
                tag_names = tag_names + ',' + tag.name
            self.setItem(row, 4, QTableWidgetItem(tag_names[1:]))

    def item_clicked(self, item):
        if item.column() == 2:
            self.edit_case(item)
        else:
            pass

    def edit_case(self, item):
        id_item = self.item(item.row(), 1)
        self.case_edit_window = CaseEdit(id_item.text())
        self.case_edit_window.setWindowModality(Qt.ApplicationModal)  # 设置QWidget为模态
        self.case_edit_window.show()

    def set_checkbox_item(self, row, column):
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        item.setTextAlignment(Qt.AlignRight)
        self.setItem(row, column, item)

    def set_table_header(self):
        for column in range(0, self.columnCount()):
            table_header_item = QTableWidgetItem(self.header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.setHorizontalHeaderItem(column, table_header_item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_layout = TableLayout('我的')
    window = QMainWindow()
    window.resize(500, 500)
    window.setCentralWidget(table_layout)
    window.show()
    app.exec_()
