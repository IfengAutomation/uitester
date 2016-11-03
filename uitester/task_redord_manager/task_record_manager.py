# @Time    : 2016/10/24 17:40
# @Author  : lixintong
import datetime

from uitester.case_manager.database import DBCommandLineHelper
from uitester.task_redord_manager.task_recorder import TaskRecorder


def get_record_by_case_id(case_id):
    '''
    获取详细record
    :param case_id:
    :return:
    '''
    task_record = DBCommandLineHelper.query_record_by_case_id(case_id)
    return task_record


def update_task_record_stats():
    '''
    更新event 统计数据
    :return:
    '''
    task_record_statses = DBCommandLineHelper.get_task_record_stats([0])
    if task_record_statses:
        for task_record_stats in task_record_statses:
            total_count = 0
            pass_count = 0
            fail_count = 0
            if task_record_stats.task_records:
                total_count = len(task_record_stats.task_records)
                for task_records in task_record_stats.task_records:
                    if task_records.status == task_records.pass_flag:
                        pass_count += 1
                    else:
                        fail_count += 1
            task_record_stats.total_count = total_count
            task_record_stats.pass_count = pass_count
            task_record_stats.fail_count = fail_count
            task_record_stats.end_time = task_record_stats.task_records[len(task_record_stats.task_records) - 1].end_time if len(
                task_record_stats.task_records) > 0 else task_record_stats.end_time
        DBCommandLineHelper.update_data()


def get_task_record_stats():
    update_task_record_stats()
    task_record_statses = DBCommandLineHelper.get_task_record_stats()
    return task_record_statses


def get_task_recorder():
    return TaskRecorder()


if __name__ == '__main__':
    runner_task = get_task_recorder()
    runner_task.add_record(1, 'device_xxxx', datetime.datetime.now(), -1,
                           expect='xxxx', log='abc')
    update_task_record_stats()
