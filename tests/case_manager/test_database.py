# @Time    : 2016/9/1 19:09
# @Author  : lixintong
import unittest

import time

from uitester.case_manager.database import DBCommandLineHelper, Tag, Case


class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.db_helper = DBCommandLineHelper()

    def test_operate_tag_data(self):
        ms_str = str(time.time())
        tag_name = "test_tag_name_" + ms_str
        tag_description = "test_tag_name_" + ms_str
        tag = self.db_helper.insert_tag(tag_name, tag_description)  # 插入tag
        dst_tag = self.db_helper.query_tag_by_id(tag.id)  # 根据tag.id 查询tag
        self.assertTrue(tag == dst_tag)
        tag_list = self.db_helper.query_tag_by_name(False, tag.name)
        self.assertTrue(tag in tag_list)

        dst_tag = self.db_helper.query_tag_by_name(True, tag.name)
        self.assertTrue(tag == dst_tag)

        tag_list = self.db_helper.query_tag_all()  # 查询所有tag
        self.assertTrue(type(tag_list[0]) is Tag)
        self.db_helper.delete_tag(tag.id)  # 删除tag
        dst_tag = self.db_helper.query_tag_by_id(tag.id)  # 根据tag.id 查询tag、
        self.assertTrue(dst_tag is None)

    def test_operate_case_data(self):
        ms_str = str(time.time())
        tag_name = "test_tag_name_" + ms_str
        tag_description = "test_tag_name_" + ms_str
        tag = self.db_helper.insert_tag(tag_name, tag_description)  # 插入tag
        tags = [tag]
        case_name = case_content = "test_case_name_" + ms_str
        case = self.db_helper.insert_case_with_tags(case_name, case_content, tags)  # 插入case
        dst_case = self.db_helper.query_case_by_id(case.id)
        self.assertTrue(case == dst_case)

        dst_case = self.db_helper.query_case_by_name(True, case.name)
        self.assertTrue(case == dst_case)

        dst_case_list = self.db_helper.query_case_by_name(False, case.name)
        self.assertTrue(case in dst_case_list)

        case_list = self.db_helper.query_case_by_tag_names([tag.name])
        self.assertTrue(type(case_list[0]) is Case)
        tag_name = "test_tag_name_" + str(time.time())

        case = self.db_helper.update_case(case.id, case.name, case.content, [tag.name], [tag_name])#todo 使用方法修改
        self.assertTrue(type(case) is Case)

        tag_name = "test_tag_name_" + str(time.time())
        case = self.db_helper.insert_case_with_tagnames(case.name, case.content, [tag.name], [tag_name])
        self.assertTrue(type(case) is Case and case.id)

        result = self.db_helper.get_table_data_by_cases_id(str(case.id))
        self.assertTrue(result['case'] and result['tag'] and result['case_tag'])

        self.db_helper.delete_case(case.id)
        dst_case = self.db_helper.query_case_by_id(case.id)
        self.assertTrue(dst_case is None)
