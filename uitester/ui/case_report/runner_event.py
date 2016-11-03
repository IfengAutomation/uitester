# @Time    : 2016/10/24 11:30
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem

from uitester.case_report_manager.case_report_manager import CaseReportManager
from uitester.ui.case_report.report import ReportWidget


class RunnerEventWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'runner_event.ui')
        uic.loadUi(ui_file_path, self)
        self.set_table_widget()

    def set_table_widget(self):
        header_text_list = ['id', '开始时间', '结束时间', '总数', '通过数', '失败数']
        self.events = CaseReportManager.get_runner_event_stats()
        row_count = len(self.events) if self.events else 0
        column_count = len(header_text_list)
        self.event_table_widget.setColumnCount(column_count)
        self.event_table_widget.setRowCount(row_count)
        self.event_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.event_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        for column in range(0, self.event_table_widget.columnCount()):
            table_header_item = QTableWidgetItem(header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.event_table_widget.setHorizontalHeaderItem(column, table_header_item)
        if self.events:
            for i, event in enumerate(self.events):
                self.event_table_widget.setItem(i, 0, QTableWidgetItem(str(event.id)))
                self.event_table_widget.setItem(i, 1, QTableWidgetItem(event.start_time.strftime("%Y-%m-%d %H:%M:%S")))
                self.event_table_widget.setItem(i, 2, QTableWidgetItem(event.end_time.strftime("%Y-%m-%d %H:%M:%S")))
                self.event_table_widget.setItem(i, 3, QTableWidgetItem(str(event.total_count)))
                self.event_table_widget.setItem(i, 4, QTableWidgetItem(str(event.pass_count)))
                self.event_table_widget.setItem(i, 5, QTableWidgetItem(str(event.fail_count)))
        self.event_table_widget.cellClicked.connect(self.cell_clicked)
        self.event_table_widget.resizeColumnsToContents()  # Adjust the width according to the content
        self.event_table_widget.horizontalHeader().setStretchLastSection(True)

    def cell_clicked(self, row, column):
        self.report_widget = ReportWidget(self.events[row].reports)
        self.report_widget.show()
