# @Time    : 2016/10/24 17:40
# @Author  : lixintong
import datetime

from uitester.case_manager.database import DBCommandLineHelper


class CaseReportManager:
    event_id = -1

    @staticmethod
    def get_init_event_id():
        '''
        插入event 并 获取初始ID
        :return:
        '''
        runner_event_stats = DBCommandLineHelper.insert_runner_event()
        CaseReportManager.event_id = runner_event_stats.id

    @staticmethod
    def add_case_report(case_id, device_id, start_time, status, **kwargs):
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
        DBCommandLineHelper.insert_report(CaseReportManager.event_id, case_id, device_id, start_time,
                                          status,
                                          str(kwargs))

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
    def update_runner_event_stats():
        '''
        更新event 统计数据
        :return:
        '''
        events = DBCommandLineHelper.get_runner_event([0])
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
                event.end_time = event.reports[len(event.reports) - 1].end_time if len(
                    event.reports) > 0 else event.end_time
            DBCommandLineHelper.update_data()

    @staticmethod
    def get_runner_event_stats():
        CaseReportManager.update_runner_event_stats()
        events = DBCommandLineHelper.get_runner_event()
        return events


# if __name__ == '__main__':
#     CaseReportManager.get_init_event_id()
#     CaseReportManager.add_case_report(1, 'device_xxxx', datetime.datetime.now(), -1,
#                                       expect='xxxx', log='abc')
#     CaseReportManager.update_runner_event_stats()
