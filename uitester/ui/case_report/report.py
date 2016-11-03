# @Time    : 2016/10/24 14:31
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

from uitester.ui.case_report.case_table_widget import QAbstractItemView, QTableWidgetItem
from uitester.ui.case_report.report_detail import ReportDetailWidget


class ReportWidget(QWidget):
    def __init__(self, reports, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'report.ui')
        uic.loadUi(ui_file_path, self)
        self.reports = reports
        self.set_table_widget()

    def set_table_widget(self):
        header_text_list = ['case_id', 'case名称', '设备id', '开始时间', '结束时间', '运行结果']
        row_count = len(self.reports) if self.reports else 0
        column_count = len(header_text_list)
        self.report_table_widget.setColumnCount(column_count)
        self.report_table_widget.setRowCount(row_count)
        self.report_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.report_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        for column in range(0, self.report_table_widget.columnCount()):
            table_header_item = QTableWidgetItem(header_text_list[column])
            table_header_item.setFont(QFont("Roman times", 12, QFont.Bold))
            self.report_table_widget.setHorizontalHeaderItem(column, table_header_item)
        if self.reports:
            for i, report in enumerate(self.reports):
                case_id = str(report.case_id) if report.case_id else ''
                case_name = report.case.name if report.case else ''
                self.report_table_widget.setItem(i, 0, QTableWidgetItem(case_id))
                self.report_table_widget.setItem(i, 1, QTableWidgetItem(case_name))
                self.report_table_widget.setItem(i, 2, QTableWidgetItem(report.device_id))
                self.report_table_widget.setItem(i, 3,
                                                 QTableWidgetItem(report.start_time.strftime("%Y-%m-%d %H:%M:%S")))
                self.report_table_widget.setItem(i, 4,
                                                 QTableWidgetItem(report.end_time.strftime("%Y-%m-%d %H:%M:%S")))
                status = '成功' if report.status == 0 else '失败'
                self.report_table_widget.setItem(i, 5, QTableWidgetItem(status))
        self.report_table_widget.cellClicked.connect(self.cell_clicked)
        self.report_table_widget.resizeColumnsToContents()  # Adjust the width according to the content
        self.report_table_widget.horizontalHeader().setStretchLastSection(True)

    def cell_clicked(self, row, column):
        self.report_detail = ReportDetailWidget(self.reports[row].message)
        self.report_detail.show()
