# @Time    : 2016/8/3 13:53
# @Author  : lixintong
import os
import zipfile

import pandas as pd

from uitester.case_data_manager.case_data_manager import CaseDataManager
from uitester.case_manager.database import DBCommandLineHelper, Case


class CaseManager:
    CASE_TABLE_NAME = "case"
    TAG_TABLE_NAME = "tag"
    CASE_TAG_TABLE_NAME = "case_tag"
    CASE_DATA_TABLE_NAME = "case_data"

    CASE_TABLE_NAME_FILE = CASE_TABLE_NAME + ".csv"
    TAG_TABLE_NAME_FILE = TAG_TABLE_NAME + ".csv"
    CASE_TAG_TABLE_NAME_FILE = CASE_TAG_TABLE_NAME + ".csv"
    CASE_DATA_TABLE_NAME_FILE = CASE_DATA_TABLE_NAME + ".csv"

    db_helper = DBCommandLineHelper()
    tag_file_data = []
    case_tag_file_data = []
    case_file_data = []
    case_data_file_data = []
    conflict_tag_name = []
    conflict_tag_message_dict = []

    def __init__(self):
        self.case_data_manager = CaseDataManager()

    def update_case(self, case_id, case_data_list,
                    delete_data_ids):
        '''
        更新case
        :return:
        '''
        self.db_helper.update_case()
        self.case_data_manager.save_case_data(case_id, case_data_list,
                                              delete_data_ids)

    def insert_case(self, case_name, content, tags, case_data_list,
                    delete_data_ids):
        '''
        插入case
        :return:
        '''
        case = self.db_helper.insert_case_with_tags(case_name, content, tags)
        self.case_data_manager.save_case_data(case.id, case_data_list,
                                              delete_data_ids)
        return case

    # 解压zip文件
    def unzip(self, path):
        zip = zipfile.ZipFile(path)
        filelist = zip.namelist()
        for file in filelist:
            f_handle = open(file, "wb")
            f_handle.write(zip.read(file))
            f_handle.close()
        zip.close()

    # 添加文件到已有的zip包中
    def addzip(self, path):
        f = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.CASE_TABLE_NAME_FILE)
        f.write(self.TAG_TABLE_NAME_FILE)
        f.write(self.CASE_TAG_TABLE_NAME_FILE)
        f.write(self.CASE_DATA_TABLE_NAME_FILE)
        f.close()
        self.remove_data_file()

    def remove_data_file(self):
        os.remove(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.CASE_DATA_TABLE_NAME_FILE))

    def export_data(self, path, case_id_list):
        cases_id = ','.join(case_id_list)
        result = self.db_helper.get_table_data_by_cases_id(cases_id)
        self.trans_to_csv(result)
        self.addzip(path)

    def trans_to_csv(self, result):
        case_data_frame = pd.DataFrame(data=list(result[self.CASE_TABLE_NAME]),
                                       columns=result[self.CASE_TABLE_NAME].keys())
        case_data_frame.to_csv(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE), encoding="utf-8", index=False)

        tag_data_frame = pd.DataFrame(data=list(result[self.TAG_TABLE_NAME]),
                                      columns=result[self.TAG_TABLE_NAME].keys())
        tag_data_frame.to_csv(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE), encoding="utf-8", index=False)

        case_tag_data_frame = pd.DataFrame(data=list(result[self.CASE_TAG_TABLE_NAME]),
                                           columns=result[self.CASE_TAG_TABLE_NAME].keys())
        case_tag_data_frame.to_csv(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE), encoding="utf-8",
                                   index=False)

        case_data_data_frame = pd.DataFrame(data=list(result[self.CASE_DATA_TABLE_NAME]),
                                            columns=result[self.CASE_DATA_TABLE_NAME].keys())

        case_data_data_frame.to_csv(os.path.join(os.getcwd(), self.CASE_DATA_TABLE_NAME_FILE), encoding="utf-8",
                                    index=False)

    # 导入数据
    def import_data(self, path):
        self.unzip(path)
        self.tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        self.case_tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))
        self.case_tag_file_data['has_changed'] = False
        self.case_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
        self.case_data_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_DATA_TABLE_NAME_FILE))

        self.remove_data_file()
        self.check_data()
        if self.conflict_tag_message_dict:
            return self.conflict_tag_message_dict
        else:
            self.merge_data()
            return None

    def merge_conflict_data_callback(self, updata_tag_message_list, callback):
        result = self.merge_conflict_data(updata_tag_message_list)
        callback(result)

    # 返回冲突修改后的信息 进行数据合并
    def merge_conflict_data(self, updata_tag_message_list):
        for tag_message in updata_tag_message_list:
            self.tag_file_data.loc[self.tag_file_data["id"] == tag_message['id'], 'name'] = tag_message['name']
            self.tag_file_data.loc[self.tag_file_data["id"] == tag_message['id'], 'description'] = tag_message[
                'description']
        self.merge_data()
        return True

    def check_data(self):
        tag_data = self.db_helper.get_table_data(self.TAG_TABLE_NAME)
        tag_db_data = pd.DataFrame(data=list(tag_data), columns=tag_data.keys())
        del self.conflict_tag_name[:]
        for name in self.tag_file_data['name']:  # 获取冲突tag名称
            if name in tag_db_data['name'].values:
                self.conflict_tag_name.append(name)
        if len(self.conflict_tag_name) > 0:  # 获取tag冲突详细信息
            conflict_message_frame = tag_db_data[tag_db_data["name"].isin(self.conflict_tag_name)]
            src_tag_message_frame = self.tag_file_data[self.tag_file_data["name"].isin(self.conflict_tag_name)]
            conflict_message_frame.loc[:, 'src_id'] = src_tag_message_frame["id"].values
            conflict_message_frame.loc[:, 'src_name'] = src_tag_message_frame["name"].values
            conflict_message_frame.loc[:, 'src_description'] = src_tag_message_frame[
                "description"].values
            self.conflict_tag_message_dict = conflict_message_frame.T.to_dict()
        return self.conflict_tag_message_dict

    # 合并数据
    def merge_data(self):
        for i in range(len(self.tag_file_data)):
            old_tag_id = self.tag_file_data["id"][i]
            tag_name = self.tag_file_data["name"][i]
            tag = self.db_helper.query_tag_by_name(tag_name)
            # 检查tag是否存在 存在的不插入 获取ID ，不存在的插入 生成ID
            if tag is None:
                tag_description = self.tag_file_data["description"][i]
                tag = self.db_helper.insert_tag(tag_name, tag_description)
            new_tag_id = tag.id
            self.case_tag_file_data.loc[
                (self.case_tag_file_data['tag_id'] == old_tag_id) & (self.case_tag_file_data['has_changed'] == False), [
                    'tag_id', 'has_changed']] = [new_tag_id, True]

        # 插入case data：
        data_id_dict = {}
        for i in range(len(self.case_data_file_data)):
            old_data_id = self.case_data_file_data['id'][i]
            data = self.case_data_file_data['data'][i]
            case_data = self.db_helper.insert_case_data(data)
            new_data_id = case_data.id
            data_id_dict[old_data_id] = new_data_id

        # 插入case 插入case_tag
        case_list = []
        for i in range(len(self.case_file_data)):
            old_case_id = self.case_file_data["id"][i]
            tag_ids = self.case_tag_file_data[self.case_tag_file_data["case_id"] == old_case_id]["tag_id"].values
            tags = []
            for tag_id in tag_ids:
                tag = self.db_helper.query_tag_by_id(int(tag_id))
                tags.append(tag)
            case = Case()
            case.name = self.case_file_data["name"][i]
            case.content = self.case_file_data["content"][i]
            case.tags = tags
            # data_relation 更新
            if self.case_file_data["data_relation"][i] and type(self.case_file_data["data_relation"][i]) is str:
                data_relation_list = eval(self.case_file_data["data_relation"][i])
                if len(data_relation_list) > 1:
                    for data_relation in data_relation_list[1:]:
                        for data_id in data_relation:
                            if data_id and data_id_dict[int(data_id)]:
                                index = data_relation.index(data_id)
                                data_relation[index] = str(data_id_dict[int(data_id)])
                    case.data_relation = self.case_data_manager.list_to_str(data_relation_list)
                    self.case_file_data["data_relation"][i] = case.data_relation

            case_list.append(case)

        self.db_helper.batch_insert_case_with_tags(case_list)

    def add_tag(self, tag_name, tag_description):
        # TODO 前端确保标识不存在
        result = {}
        tag = self.db_helper.query_tag_by_name(tag_name)
        if tag:
            result['status'] = -1
            result['message'] = '标识已存在'
        else:
            self.db_helper.insert_tag(tag_name, tag_description)
            result['status'] = 0
            result['message'] = '标识插入成功'
        return result

    def query_case_data(self, case=None, case_id=None):
        '''
        get case data driven
        :param case_id:
        :return:
        '''

        if case == None:
            case = self.db_helper.query_case_by_id(case_id)
        if case and case.data_relation:
            del case.data[:]
            data_relation_list = eval(case.data_relation)
            case.data.append(data_relation_list[0])
            if len(data_relation_list) > 1:
                for data_relation in data_relation_list[1:]:
                    data_list = []
                    for data_id in data_relation:
                        if data_id != '-1':
                            case_data = self.db_helper.query_case_data(id=data_id)
                            data_list.append(case_data.data)
                        else:
                            data_list.append('')
                    case.data.append(data_list)
        return case

    def update_data_header(self, oper_type, case, old_header_name, new_header_name):
        if oper_type == 'add':
            case.data[0].append(new_header_name)
            data_relation_list = eval(case.data_relation)
            data_relation_list[0].append(new_header_name)
            for data in data_relation_list[1:]:
                data.append('-1')
            case.data_relation = self.list_to_str(data_relation_list)
        elif oper_type == 'modify':
            index = case.data[0].index(old_header_name)
            case.data[0][index] = new_header_name
            case.data_relation.replace(old_header_name, new_header_name)
        elif oper_type == 'delete':
            index = case.data[0].index(old_header_name)
            for data in case.data:
                del data[index]
            data_relation_list = eval(case.data_relation)
            index = data_relation_list[0].index(old_header_name)
            for data_relation in data_relation_list:
                del data_relation[index]
            case.data_relation = self.list_to_str(data_relation_list)
        self.db_helper.update_case()

    def list_to_str(self, data_list):
        '''
        two-dimensional array to string
        string [[],[],[]]
        :return:
        '''
        data_relation_str = '['
        for data in data_list:
            data_relation_str += '['
            for column in data:
                data_relation_str = data_relation_str + '\'' + column + '\','
            data_relation_str = data_relation_str[:len(data_relation_str) - 1]
            data_relation_str += '],'
        data_relation_str = data_relation_str[:len(data_relation_str) - 1]
        data_relation_str += ']'
        return data_relation_str
