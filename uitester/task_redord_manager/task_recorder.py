# @Time    : 2016/11/3 15:12
# @Author  : lixintong
from uitester.case_manager.database import DBCommandLineHelper


class TaskRecorder:
    def __init__(self):
        task_record_stats = DBCommandLineHelper.insert_task_record_stats()
        self.task_id = task_record_stats.id

    def add_record(self, case_id, device_id, start_time, status, **kwargs):
        DBCommandLineHelper.insert_record(self.task_id, case_id, device_id, start_time,
                                          status,
                                          str(kwargs))
