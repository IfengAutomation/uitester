# @Time    : 2016/9/28 17:24
# @Author  : lixintong

from uitester.case_manager.database import DBCommandLineHelper, CaseData


class CaseDataManager:
    def __init__(self):
        self.db_helper = DBCommandLineHelper()

    def get_case_data_count(self, case_id):
        case = self.db_helper.query_case_by_id(case_id)
        count = 0
        if case.data_relation:
            data_relation_list = eval(case.data_relation)
            for data_relation in data_relation_list[1:]:
                for data in data_relation:
                    if data:
                        count += 1
                        break
        return count

    def get_case_data(self, case_id):
        case_data_list = []
        case = self.db_helper.query_case_by_id(case_id)
        if case.data_relation is not None and case.data_relation:
            data_relation_list = eval(case.data_relation)
            case_data_list.append(data_relation_list[0])
            for data_relation in data_relation_list[1:]:
                temp_data_list = []
                for data_id in data_relation:
                    case_data = CaseData()
                    if data_id:
                        temp_case_data = self.db_helper.query_case_data(id=int(data_id))
                        case_data.id = temp_case_data.id
                        case_data.data = temp_case_data.data
                        case_data.init_data = temp_case_data.data
                    temp_data_list.append(case_data)
                case_data_list.append(temp_data_list)
        return case_data_list

    def get_format_case_data(self, row_count, column_count, case_id):
        case_data_list = []
        db_case_data_list = []
        if case_id:
            db_case_data_list = self.get_case_data(case_id)
        # header:
        db_case_data_len = len(db_case_data_list)
        for row_num in range(0, row_count):
            temp_list = []
            for column_num in range(0, column_count):
                if db_case_data_list and row_num < db_case_data_len and column_num < len(db_case_data_list[row_num]):
                    temp_list.append(db_case_data_list[row_num][column_num])
                else:
                    if row_num == 0:
                        temp_list.append('')
                    else:
                        temp_list.append(CaseData())
            case_data_list.append(temp_list)
        return case_data_list

    def save_case_data(self, case_id, case_data_list, delete_data_ids):
        case = self.db_helper.query_case_by_id(case_id)
        case_relation_list = []
        for case_data in case_data_list:
            for case_data_detail in case_data:
                if type(case_data_detail) == CaseData:
                    if case_data_detail.id and case_data_detail.data != case_data_detail.init_data and case_data_detail.data != '':  # 修改
                        self.db_helper.update_case_data(case_data_detail.id, case_data_detail.data)
                    elif case_data_detail.data == '' or case_data_detail.data is None and case_data_detail.id:  # 删除
                        self.db_helper.delete_case_data(id=case_data_detail.id)
                        case_data_detail.id = None
                        case_data_detail.data = ''
                    elif case_data_detail.id is None and case_data_detail.data:  # 添加 检验id 值
                        add_case_data = self.db_helper.insert_case_data(data=case_data_detail.data)
                        case_data_detail.id = add_case_data.id
                    case_data_detail.init_data = case_data_detail.data
        # 获取 case relation
        for case_data in case_data_list:
            temp_list = []
            for case_data_detail in case_data:
                if type(case_data_detail) == CaseData:
                    id = '' if case_data_detail.id is None else str(case_data_detail.id)
                    temp_list.append(id)
                else:
                    temp_list.append(case_data_detail)
            case_relation_list.append(temp_list)
        case.data_relation = self.list_to_str(case_relation_list)
        self.db_helper.update_case()
        # 删除 case data
        if delete_data_ids:
            self.db_helper.batch_delete_case_data(delete_data_ids)

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