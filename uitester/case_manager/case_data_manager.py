# @Time    : 2016/8/3 13:53
# @Author  : lixintong
import os
import zipfile

import pandas as pd

from uitester.case_manager.database import DBCommandLineHelper, Case


class CaseDataManager:
    CASE_TABLE_NAME = "case"
    TAG_TABLE_NAME = "tag"
    CASE_TAG_TABLE_NAME = "case_tag"
    CASE_TABLE_NAME_FILE = CASE_TABLE_NAME + ".csv"
    TAG_TABLE_NAME_FILE = TAG_TABLE_NAME + ".csv"
    CASE_TAG_TABLE_NAME_FILE = CASE_TAG_TABLE_NAME + ".csv"
    db_helper = DBCommandLineHelper()
    tag_file_data = []
    case_tag_file_data = []
    case_file_data = []
    conflict_tag_name = []
    conflict_tag_message_dict = []

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
        f.close()
        self.remove_data_file()

    def remove_data_file(self):
        os.remove(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))

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

    # 导入数据
    def import_data(self, path):
        self.unzip(path)
        self.tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        self.case_tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))
        self.case_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
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
            self.case_tag_file_data.loc[self.case_tag_file_data['tag_id'] == old_tag_id, 'tag_id'] = new_tag_id
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

    def query_case_data_driven(self, case,id=None):
        '''
        get case data driven by case id
        :param case_id:
        :return:
        '''
        if case.data_driven_relation:
            case.case_data_driven = eval(case.data_driven_relation)
        return case
        # case = self.db_helper.query_case_by_id(case_id)
        # if case.data_driven_relation:
        #     data_driven_relation = eval(case.data_driven_relation)  # 字符串转二维数组
        #     print("data_driven_relation:{}".format(data_driven_relation))  # todo 可能为空   对空做处理
        #     if len(data_driven_relation) > 0:
        #         print("len data_driven_relation:{}".format(len(data_driven_relation)))
        #         data_driven_column = data_driven_relation[0]
        #         for row in range(1, len(data_driven_relation)):
        #             for column in range(0, len(data_driven_column)):
        #                 data_driven_id = data_driven_relation[row][column]
        #                 data = self.db_helper.query_case_data_driven_by_id(int(data_driven_id))
        #                 print("data:{}".format(data))
        #                 case.case_data_driven[data_driven_column[column]] = data

                    # return case

    def insert_case_data_driven(self):
        # 如果插入后没保存怎么办，
        # todo 参数case_id
        # 更新case 中的 data_driven_relation
        # 插入 case_data_dirven 数据
        #
        self.db_helper.insert_case_data_driven()

    def modify_case_data_driven(self, id):
        '''
        modify case data driven
        :param id:
        :return:
        '''
        self.db_helper.modify_case_data_driven()

    def delete_case_data_driven(self):
        pass

    def save_case_data_driven(self):
        pass


if __name__ == '__main__':
    case_data_manager = CaseDataManager()
    case = case_data_manager.db_helper.query_case_by_id(1)
    case = case_data_manager.query_case_data_driven(case = case)
    print(case)