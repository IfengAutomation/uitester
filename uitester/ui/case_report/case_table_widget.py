# @Time    : 2016/9/9 16:47
# @Author  : lixintong

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import *

from uitester.config import Config


class CaseTableWidget(QWidget):
    def __init__(self, case_list, result, hide_column_list=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.dataTableWidget = DataTableWidget(hide_column_list, case_list,result)  # init ui table
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.dataTableWidget)
        self.setLayout(layout)
        self.checked_cases_message = []
        self.result = result

    def get_checked_data(self):
        del self.checked_cases_message[:]
        for row_num in range(0, self.dataTableWidget.rowCount()):
            checkbox_item = self.dataTableWidget.item(row_num, 0)
            if checkbox_item.checkState() == Qt.Checked:
                case_id = self.dataTableWidget.item(row_num, 1).text()
                self.checked_cases_message.append({"case_id": case_id, "row_num": row_num})


class DataTableWidget(QTableWidget):
    header_text_list = ['', 'id', '名称', '最后修改时间', '标识', '运行结果']
    column_count = len(header_text_list)

    def __init__(self, hide_column_list, case_list,result, *args):
        super().__init__(*args)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setObjectName("data_table_widget")
        self.result = result
        self.case_list = case_list
        self.setRowCount(len(self.case_list))
        self.setColumnCount(self.column_count)
        self.set_table_data()
        self.check_all = False
        if hide_column_list is not None:
            for column in hide_column_list:
                self.hideColumn(column)

    def set_checkbox_item(self, row, column):
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        item.setCheckState(Qt.Unchecked)
        item.setTextAlignment(Qt.AlignRight)
        self.setItem(row, column, item)

    def set_table_header(self):
        item = QTableWidgetItem()
        config = Config()
        item.setIcon(QIcon(QPixmap(config.images + '/check_all.png')))
        self.setHorizontalHeaderItem(0, item)
        for column in range(1, self.columnCount()):
            table_header_item = QTableWidgetItem(self.header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.setHorizontalHeaderItem(column, table_header_item)
        self.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        self.horizontalHeader().sectionClicked.connect(self.horsection_clicked)  # 表头单击信号

    def set_table_data(self):
        self.set_table_header()
        for row in range(0, self.rowCount()):
            self.set_checkbox_item(row, 0)
            case = self.case_list[row]
            self.setItem(row, 1, QTableWidgetItem(str(case.id)))
            self.setItem(row, 2, QTableWidgetItem(case.name))
            self.setItem(row, 3, QTableWidgetItem(case.last_modify_time.strftime("%Y-%m-%d %H:%M:%S")))
            result = '成功' if self.result[row] == 1 else '失败'
            tag_names = ''
            for tag in case.tags:
                tag_names = tag_names + ',' + tag.name
            self.setItem(row, 4, QTableWidgetItem(tag_names[1:]))
            self.setItem(row, 5, QTableWidgetItem(result))
        self.resizeColumnsToContents()  # Adjust the width according to the content
        self.horizontalHeader().setStretchLastSection(True)

    def horsection_clicked(self, index):
        if index == 0:
            if self.check_all:
                check_status = Qt.Unchecked
                self.check_all = False
            else:
                check_status = Qt.Checked
                self.check_all = True
            for row in range(0, self.rowCount()):
                check_box_item = self.item(row, 0)
                check_box_item.setCheckState(check_status)
