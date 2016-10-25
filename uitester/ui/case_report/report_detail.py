# @Time    : 2016/10/24 14:31
# @Author  : lixintong
import os

import pandas as pd
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from uitester.case_report_manager.case_report_manager import CaseReportManager
from uitester.ui.case_report.case_table_widget import CaseTableWidget


class ReportDetail(QWidget):
    def __init__(self, report_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        case_report_manager = CaseReportManager()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'report_detail.ui')
        uic.loadUi(ui_file_path, self)
        data_file_path = os.path.join(ui_dir_path, 'report_detail.csv')
        self.report_detail_data = pd.read_csv(data_file_path)
        report_details = self.report_detail_data[self.report_detail_data["report_id"] == report_id][
            "case_ids"].values
        case_results = self.report_detail_data[self.report_detail_data["report_id"] == report_id][
            "result"].values
        case_results = [int(i) for i in case_results[0].split(',')]
        if report_details:
            case_ids = [int(i) for i in report_details[0].split(',')]
            case_list = case_report_manager.get_cases_by_ids(case_ids)
            case_table_widget = CaseTableWidget(case_list,case_results, [0])
            self.main_layout.insertWidget(1, case_table_widget)
