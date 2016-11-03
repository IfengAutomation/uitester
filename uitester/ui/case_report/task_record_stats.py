# @Time    : 2016/10/24 11:30
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem

from uitester.task_redord_manager.task_record_manager import get_task_record_stats
from uitester.ui.case_report.task_record import TaskRecordWidget


class RunnerEventWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'task_record_stats.ui')
        uic.loadUi(ui_file_path, self)
        self.set_table_widget()

    def set_table_widget(self):
        header_text_list = ['id', '开始时间', '结束时间', '总数', '通过数', '失败数']
        self.task_record_statses = get_task_record_stats()
        row_count = len(self.task_record_statses) if self.task_record_statses else 0
        column_count = len(header_text_list)
        self.event_table_widget.setColumnCount(column_count)
        self.event_table_widget.setRowCount(row_count)
        self.event_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.event_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        for column in range(0, self.event_table_widget.columnCount()):
            table_header_item = QTableWidgetItem(header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.event_table_widget.setHorizontalHeaderItem(column, table_header_item)
        if self.task_record_statses:
            for i, task_record_stats in enumerate(self.task_record_statses):
                self.event_table_widget.setItem(i, 0, QTableWidgetItem(str(task_record_stats.id)))
                self.event_table_widget.setItem(i, 1, QTableWidgetItem(
                    task_record_stats.start_time.strftime("%Y-%m-%d %H:%M:%S")))
                self.event_table_widget.setItem(i, 2, QTableWidgetItem(
                    task_record_stats.end_time.strftime("%Y-%m-%d %H:%M:%S")))
                self.event_table_widget.setItem(i, 3, QTableWidgetItem(str(task_record_stats.total_count)))
                self.event_table_widget.setItem(i, 4, QTableWidgetItem(str(task_record_stats.pass_count)))
                self.event_table_widget.setItem(i, 5, QTableWidgetItem(str(task_record_stats.fail_count)))
        self.event_table_widget.cellClicked.connect(self.cell_clicked)
        self.event_table_widget.resizeColumnsToContents()  # Adjust the width according to the content
        self.event_table_widget.horizontalHeader().setStretchLastSection(True)

    def cell_clicked(self, row, column):
        self.report_widget = TaskRecordWidget(self.task_record_statses[row].task_records)
        self.report_widget.show()
