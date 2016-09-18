# @Time    : 2016/8/22 13:46
# @Author  : lixintong
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from uitester.ui.case_manager.case_editor import EditorWidget


class TableWidget(QWidget):
    def __init__(self, show_case_editor_signal, tester, case_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_case_editor_signal = show_case_editor_signal
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dataTableWidget = DataTableWidget(self.show_case_editor_signal, tester, case_list)  # init ui table
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.dataTableWidget)
        self.setLayout(layout)
        self.checked_cases_message = []
        self.check_all = False

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

    def __init__(self, show_case_editor_signal, tester, case_list, *args):
        super().__init__(*args)
        self.show_case_editor_signal = show_case_editor_signal
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tester = tester
        self.setObjectName("data_table_widget")
        self.case_list = case_list
        self.setRowCount(len(self.case_list))
        self.setColumnCount(self.column_count)
        self.set_table_data()
        self.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self, row, column):
        if column != 0:
            id_item = self.item(row, 1)
            self.show_case_editor_signal.emit(1, int(id_item.text()))

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
        self.resizeColumnsToContents()
        self.horizontalHeader().setStretchLastSection(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    table_layout = TableWidget('我的')
    window = QMainWindow()
    window.resize(500, 500)
    window.setCentralWidget(table_layout)
    window.show()
    app.exec_()
