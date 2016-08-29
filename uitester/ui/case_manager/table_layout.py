# @Time    : 2016/8/22 13:46
# @Author  : lixintong
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from uitester.ui.case_manager.case_editor import EditorWidget


class TableLayout(QWidget):
    def __init__(self, case_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 4, screen.height() / 4)
        self.dataTableWidget = DataTableWidget(case_list)  # 根据查询条件获取table data
        layout = QVBoxLayout()
        layout.addWidget(self.dataTableWidget)
        self.setLayout(layout)
        self.checked_cases_message = []  # 待删除Id



    def get_checked_data(self):
        del self.checked_cases_message[:]
        for row_num in range(0, self.dataTableWidget.rowCount()):
            checkbox_item = self.dataTableWidget.item(row_num, 0)
            if checkbox_item.checkState() == Qt.Checked:
                case_id = self.dataTableWidget.item(row_num, 1).text()
                self.checked_cases_message.append({"case_id": case_id, "row_num": row_num})


class DataTableWidget(QTableWidget):
    header_text_list = ['', 'id', '名称', '最后修改时间', '标识']
    column_count = len(header_text_list)

    def __init__(self, case_list, *args):
        super().__init__(*args)
        self.setObjectName("data_table_widget")
        self.case_list = case_list
        self.setRowCount(len(self.case_list))
        self.setColumnCount(self.column_count)
        self.set_table_data()

    def item_clicked(self, item):
        if item.column() == 2:
            self.edit_case(item)

    def edit_case(self, item):
        id_item = self.item(item.row(), 1)
        self.case_edit_window = EditorWidget(id_item.text())
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
        self.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        # self.horizontalHeader().sectionClicked.connect(self.hor_sction_clicked)  # 表头单击信号

    def set_table_data(self):
        # self.case_list = case_list
        # self.setRowCount(len(self.case_list))
        # self.setColumnCount(self.column_count)
        self.itemClicked.connect(self.item_clicked)
        self.set_table_header()
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
        self.resizeColumnsToContents()  # 根据内容调整行的宽度
        self.setStyleSheet("selection-background-color:#0066CC;")
        self.horizontalHeader().setStretchLastSection(True)
        # self.resizeRowToContents(0)  # 根据内容调整列的宽度度

    # def hor_sction_clicked(self,index):
    #     print(index)
    #     if index == 0:
    #         self.check_or_cancel_all()
    #
    # def check_or_cancel_all(self):
    #     header_item = self.horizontalHeaderItem(0)
    #     check_status = Qt.Checked
    #     if header_item.text()=='全选':
    #         header_item.setText("取消")
    #     else:
    #         header_item.setText("全选")
    #         check_status = Qt.Unchecked
    #     for row in range(0, self.rowCount()):
    #         check_box_item = self.item(row, 0)
    #         check_box_item.setCheckState(check_status)
        # self.resizeColumnsToContents()
        # self.set_table_header()
        # self.horizontalHeader().setStretchLastSection(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_layout = TableLayout('我的')
    window = QMainWindow()
    window.resize(500, 500)
    window.setCentralWidget(table_layout)
    window.show()
    app.exec_()
