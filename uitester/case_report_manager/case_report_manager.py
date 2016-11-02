# @Time    : 2016/10/24 17:40
# @Author  : lixintong
import datetime

from uitester.case_manager.database import DBCommandLineHelper


class CaseReportManager:
    def __init__(self):
        self.db_helper = DBCommandLineHelper()

    def get_cases_by_ids(self, ids):
        return self.db_helper.query_cases_by_ids(ids)

    @staticmethod
    def get_init_event_id():
        '''
        插入event 并 获取初始ID
        :return:
        '''
        runner_event_stats = DBCommandLineHelper.insert_runner_event()
        return runner_event_stats.id

    @staticmethod
    def add_case_report(event_id, case_id, device_id, start_time, end_time, status, message):
        '''
        插入report
        :param event_id:
        :param case_id:
        :param device_id:
        :param start_time:
        :param end_time:
        :param status:
        :param message:
        :return:
        '''
        DBCommandLineHelper.insert_report(event_id, case_id, device_id, start_time, end_time,
                                          status,
                                          str(message))


        # 删除数据-- 删除case 的时候

    @staticmethod
    def get_report_by_case_id(case_id):
        '''
        获取详细report
        :param case_id:
        :return:
        '''
        report = DBCommandLineHelper.query_report_by_case_id(case_id)
        return report

    @staticmethod
    def runner_event_stats():
        '''
        更新event 统计数据
        :return:
        '''
        events = DBCommandLineHelper.get_runner_event()
        if events:
            for event in events:
                total_count = 0
                pass_count = 0
                fail_count = 0
                if event.reports:
                    total_count = len(event.reports)
                    for report in event.reports:
                        if report.status == report.pass_flag:
                            pass_count += 1
                        else:
                            fail_count += 1
                event.total_count = total_count
                event.pass_count = pass_count
                event.fail_count = fail_count
            DBCommandLineHelper.update_data()

# if __name__ == '__main__':
    # event_id = CaseReportManager.get_init_event_id()
    # CaseReportManager.add_case_report(2, 1, 'device_xxxx', datetime.datetime.now(), datetime.datetime.now(), 0,
    #                                   {'expect': 'xxxx'})
    # CaseReportManager.runner_event_stats()

