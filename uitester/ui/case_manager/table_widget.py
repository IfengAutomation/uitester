# @Time    : 2016/8/22 13:46
# @Author  : lixintong
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from uitester.ui.case_manager.case_editor import EditorWidget


class TableWidget(QWidget):
    def __init__(self, refresh_data, tester, case_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_data = refresh_data
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dataTableWidget = DataTableWidget(self.refresh_data, tester, case_list)  # init ui table
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.dataTableWidget)
        self.setLayout(layout)
        self.checked_cases_message = []

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

    def __init__(self, refresh_data, tester, case_list, *args):
        super().__init__(*args)
        self.refresh_data = refresh_data
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tester = tester
        self.setObjectName("data_table_widget")
        self.case_list = case_list
        self.setRowCount(len(self.case_list))
        self.setColumnCount(self.column_count)
        self.set_table_data()

    def item_clicked(self, item):
        if item.column() == 2:
            self.edit_case(item)

    def cell_clicked(self, row, column):
        if column == 2:
            id_item = self.item(row, 1)
            self.case_edit_window = EditorWidget(self.refresh_data, self.tester, id_item.text())
            self.case_edit_window.show()

    def edit_case(self, item):
        id_item = self.item(item.row(), 1)
        self.case_edit_window = EditorWidget(self.tester, id_item.text())
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

    def set_table_data(self):
        # self.itemClicked.connect(self.item_clicked)
        self.cellDoubleClicked.connect(self.cell_clicked)
        self.set_table_header()
        for row in range(0, self.rowCount()):
            self.set_checkbox_item(row, 0)
            case = self.case_list[row]
            self.setItem(row, 1, QTableWidgetItem(str(case.id)))
            case_name_label = QLabel()
            case_name_label.setText("<font color=#0072E3><u>{}</u></font>".format(case.name))
            self.setCellWidget(row, 2, case_name_label)
            # self.setItem(row, 2,QTableWidgetItem(case.name))
            self.setItem(row, 3, QTableWidgetItem(case.last_modify_time.strftime("%Y-%m-%d %H:%M:%S")))
            tag_names = ''
            for tag in case.tags:
                tag_names = tag_names + ',' + tag.name
            self.setItem(row, 4, QTableWidgetItem(tag_names[1:]))
        self.resizeColumnsToContents()  # Adjust the width according to the content
        # self.setStyleSheet("selection-background-color:#0066CC;")
        self.horizontalHeader().setStretchLastSection(True)

    def label_clicked(self):
        print('label clicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_layout = TableWidget('我的')
    window = QMainWindow()
    window.resize(500, 500)
    window.setCentralWidget(table_layout)
    window.show()
    app.exec_()
