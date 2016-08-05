# @Time    : 2016/8/3 13:53
# @Author  : lixintong
import os
import zipfile
import pandas as pd

from uitester.case_manager.database import DBCommandLineHelper


class CaseManager:
    CASE_TABLE_NAME = "case"
    TAG_TABLE_NAME = "tag"
    CASE_TAG_TABLE_NAME = "case_tag"
    CASE_TABLE_NAME_FILE = CASE_TABLE_NAME + ".csv"
    TAG_TABLE_NAME_FILE = TAG_TABLE_NAME + ".csv"
    CASE_TAG_TABLE_NAME_FILE = CASE_TAG_TABLE_NAME + ".csv"
    ZIP_NAME = "data.zip"
    db_command_line_helper = DBCommandLineHelper()
    tag_file_data = []
    case_tag_file_data = []
    case_file_data = []
    conflict_tag_name = []
    conflict_tag_message_list = []

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
        f = zipfile.ZipFile(os.path.join(path, self.ZIP_NAME), 'w', zipfile.ZIP_DEFLATED)
        f.write(self.CASE_TABLE_NAME_FILE)
        f.write(self.TAG_TABLE_NAME_FILE)
        f.write(self.CASE_TAG_TABLE_NAME_FILE)
        f.close()
        self.remove_data_file()

    def remove_data_file(self):
        os.getcwd()
        os.remove(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        os.remove(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))

    # 导出数据
    def export_all_data(self, path):
        self.export_data_by_name(self.CASE_TABLE_NAME, self.CASE_TABLE_NAME_FILE)
        self.export_data_by_name(self.TAG_TABLE_NAME, self.TAG_TABLE_NAME_FILE)
        self.export_data_by_name(self.CASE_TAG_TABLE_NAME, self.CASE_TAG_TABLE_NAME_FILE)
        self.addzip(path)

    def export_data_by_name(self, table_name, table_file_name):
        case_data = self.db_command_line_helper.get_table_data(table_name)
        case_data_frame = pd.DataFrame(data=list(case_data), columns=case_data.keys())
        case_data_frame.to_csv(os.path.join(os.getcwd(), table_file_name), encoding="utf-8", index=False)

    # 导入数据
    def import_data(self):
        self.tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.TAG_TABLE_NAME_FILE))
        self.case_tag_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TAG_TABLE_NAME_FILE))
        self.case_file_data = pd.read_csv(os.path.join(os.getcwd(), self.CASE_TABLE_NAME_FILE))
        self.check_data()
        if len(self.conflict_tag_message_list) > 0:
            return self.conflict_tag_message_list
        else:
            self.merge_data()

    # 返回冲突修改后的信息 进行数据合并
    def merge_conflict_data(self, updata_tag_message_list):
        for tag_message in updata_tag_message_list:
            self.tag_file_data.loc[self.tag_file_data["id"] == tag_message['id'], 'name'] = tag_message['name']
            self.tag_file_data.loc[self.tag_file_data["id"] == tag_message['id'], 'description'] = tag_message[
                'description']
        self.merge_data()

    def check_data(self):
        tag_data = self.db_command_line_helper.get_table_data(self.TAG_TABLE_NAME)
        tag_db_data = pd.DataFrame(data=list(tag_data), columns=tag_data.keys())
        del self.conflict_tag_name[:]
        del self.conflict_tag_message_list[:]
        for name in self.tag_file_data['name']:  # 获取冲突tag名称
            if name in tag_db_data['name'].values:
                self.conflict_tag_name.append(name)
        if len(self.conflict_tag_name) > 0:  # 获取tag冲突详细信息
            conflict_message_frame = tag_db_data[tag_db_data["name"].isin(self.conflict_tag_name)]
            src_tag_message_frame = self.tag_file_data[self.tag_file_data["name"].isin(self.conflict_tag_name)]
            conflict_message_frame['src_id'] = src_tag_message_frame["id"].values
            conflict_message_frame['src_name'] = src_tag_message_frame["name"].values
            conflict_message_frame['src_description'] = src_tag_message_frame[
                "description"].values
            self.conflict_tag_message_list = conflict_message_frame.T.to_dict().values()
        return self.conflict_tag_message_list

    #合并数据
    def merge_data(self):
        for i in range(len(self.tag_file_data)):
            old_tag_id = self.tag_file_data["id"][i]
            tag_name = self.tag_file_data["name"][i]
            tag = self.db_command_line_helper.query_tag_by_name(True, tag_name)
            # 检查tag是否存在 存在的不插入 获取ID ，不存在的插入 生成ID
            if tag is None:
                tag_description = self.tag_file_data["description"][i]
                tag = self.db_command_line_helper.insert_tag(tag_name, tag_description)
            new_tag_id = tag.id
            self.case_tag_file_data.loc[self.case_tag_file_data['tag_id'] == old_tag_id, 'tag_id'] = new_tag_id
        # 插入case 插入case_tag
        for i in range(len(self.case_file_data)):
            old_case_id = self.case_file_data["id"][i]
            tag_ids = self.case_tag_file_data[self.case_tag_file_data["case_id"] == old_tag_id]["tag_id"].values
            tags = []
            for tag_id in tag_ids:
                tag = self.db_command_line_helper.query_tag_by_id(int(tag_id))
                tags.append(tag)
            case = self.db_command_line_helper.insert_case(self.case_file_data["name"][i],
                                                           self.case_file_data["content"][i],
                                                           tags)
            new_case_id = case.id
            self.case_tag_file_data.loc[self.case_tag_file_data['case_id'] == old_case_id, 'case_id'] = new_case_id
        self.remove_data_file()

    def test_export_data(self):
        path = 'C:/Users/Fredric/Desktop/新建文件夹'
        self.export_all_data(path)

    def testimport_data(self):
        caseManager.unzip("C:/Users/Fredric/Desktop/新建文件夹/data.zip")
        updata_tag_message_list = caseManager.import_data()
        if updata_tag_message_list is not None:
            caseManager.merge_conflict_data(updata_tag_message_list)


if __name__ == '__main__':
    caseManager = CaseManager()
    # caseManager.test_export_data()
    caseManager.testimport_data()
    # caseManager.test()
    # caseManager.export_all_data("C:/Users/Fredric/Desktop/新建文件夹")
    # caseManager.unzip("C:/Users/Fredric/Desktop/新建文件夹/data.zip")

