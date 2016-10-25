# @Time    : 2016/10/24 11:30
# @Author  : lixintong
import os

import pandas as pd
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem

from uitester.ui.case_report.report_detail import ReportDetail


class ReportWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_report.ui')
        uic.loadUi(ui_file_path, self)
        # 从文件读取
        self.row_count = 10
        self.column_count = 5
        self.set_table_widget()

    def set_table_widget(self):
        header_text_list = ['id', '时间', '总数', '通过数', '失败数']
        column_count = len(header_text_list)
        self.report_table_widget.setColumnCount(column_count)
        self.report_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.report_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        for column in range(0, self.report_table_widget.columnCount()):
            table_header_item = QTableWidgetItem(header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.report_table_widget.setHorizontalHeaderItem(column, table_header_item)

        # 读取文件
        ui_dir_path = os.path.dirname(__file__)
        data_file_path = os.path.join(ui_dir_path, 'report_data.csv')
        self.report_file_data = pd.read_csv(data_file_path)
        self.report_table_widget.setRowCount(len(self.report_file_data))
        for i in range(len(self.report_file_data)):
            self.report_table_widget.setItem(i, 0, QTableWidgetItem(str(self.report_file_data["id"][i])))
            self.report_table_widget.setItem(i, 1, QTableWidgetItem(self.report_file_data["date"][i]))
            self.report_table_widget.setItem(i, 2, QTableWidgetItem(str(self.report_file_data["total"][i])))
            self.report_table_widget.setItem(i, 3, QTableWidgetItem(str(self.report_file_data["ok"][i])))
            self.report_table_widget.setItem(i, 4, QTableWidgetItem(str(self.report_file_data["failure"][i])))
        self.report_table_widget.cellClicked.connect(self.cell_clicked)
        self.report_table_widget.resizeColumnsToContents()  # Adjust the width according to the content
        self.report_table_widget.horizontalHeader().setStretchLastSection(True)

    def cell_clicked(self, row, column):
        item = self.report_table_widget.item(row, 0)
        self.report_detail = ReportDetail(int(item.text()))
        self.report_detail.show()
