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
        os.remove(self.CASE_TABLE_NAME_FILE)
        os.remove(self.TAG_TABLE_NAME_FILE)
        os.remove(self.CASE_TAG_TABLE_NAME_FILE)

    def export_all_data(self,path):
        '''导出数据'''  # todo 能否一次性全部导出
        dBCommandLineHelper = DBCommandLineHelper()
        self.export_data_by_name(dBCommandLineHelper, self.CASE_TABLE_NAME, self.CASE_TABLE_NAME_FILE)
        self.export_data_by_name(dBCommandLineHelper, self.TAG_TABLE_NAME, self.TAG_TABLE_NAME_FILE)
        self.export_data_by_name(dBCommandLineHelper, self.CASE_TAG_TABLE_NAME, self.CASE_TAG_TABLE_NAME_FILE)
        self.addzip(path)

    def export_data_by_name(self, dBCommandLineHelper, table_name, table_file_name):
        case_data = dBCommandLineHelper.get_table_data(table_name)
        case_data_frame = pd.DataFrame(data=list(case_data), columns=case_data.keys())
        case_data_frame.to_csv(os.path.join(os.getcwd(), table_file_name), index=False)

    def import_data(self):
        '''导入数据'''
        pass

    def check_data(self):
        '''检测数据'''

        pass

    def merge_data(self):
        '''合并数据'''
        pass

    def test(self):
        path = 'C:/Users/Fredric/Desktop/新建文件夹'
        self.export_all_data(path)

if __name__ == '__main__':
    caseManager = CaseManager()
    caseManager.test()
