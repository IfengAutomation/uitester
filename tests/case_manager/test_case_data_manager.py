# @Time    : 2016/9/1 21:04
# @Author  : lixintong
import datetime
import os
import unittest

from uitester.case_manager.case_data_manager import CaseDataManager


class TestCaseDataManager(unittest.TestCase):
    def setUp(self):
        self.case_data_manager = CaseDataManager()
        self.package_name = ''

    def test_export_and_import_data(self):
        # notice export and import must has common CaseDataManager
        # export test
        print(" export start :", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        case_list = self.case_data_manager.db_helper.query_case_all()
        cases_id_list = []
        for case in case_list:
            cases_id_list.append(str(case.id))  # 类型转成str
        path = os.path.join(os.getcwd(),'data.dpk')
        # self.package_name = self.case_data_manager.export_data(path, cases_id_list)
        self.case_data_manager.export_data(path, cases_id_list)#导入数据
        print(" export finish :", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # import test
        print(" import start :", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        conflict_datas = self.case_data_manager.import_data(path)#有冲突
        conflict_datas = self.case_data_manager.import_data(path)  # 无冲突
        if conflict_datas:
            updata_tag_message_list = []
            for key in conflict_datas:
                data = conflict_datas[key]
                updata_tag_message_list.append(data)
            self.case_data_manager.merge_conflict_data(updata_tag_message_list)  # result validation unfinished
            print(self.case_data_manager.case_file_data["name"][0])
            case = self.case_data_manager.db_helper.query_case_by_name(True,
                                                                       self.case_data_manager.case_file_data[
                                                                                       "name"][0])

        self.assertTrue(case is not None)
        print("import finish :", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
