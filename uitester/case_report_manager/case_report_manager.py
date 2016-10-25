# @Time    : 2016/10/24 17:40
# @Author  : lixintong
from uitester.case_manager.database import DBCommandLineHelper


class CaseReportManager:
    def __init__(self):
        self.db_helper = DBCommandLineHelper()

    def get_cases_by_ids(self, ids):
        return self.db_helper.query_cases_by_ids(ids)
