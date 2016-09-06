# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from uitester.case_manager.case_data_manager import CaseDataManager
from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_editor import EditorWidget
from uitester.ui.case_manager.case_search_edit import TagCompleter, TagLineEdit, SearchButton
from uitester.ui.case_manager.conflict_tag import ConflictTagsWidget
from uitester.ui.case_manager.table_layout import TableLayout


class CaseManagerWidget(QWidget):
    def __init__(self, tester, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_helper = DBCommandLineHelper()
        self.case_data_manager = CaseDataManager()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_manager.ui')
        uic.loadUi(ui_file_path, self)
        self.add_case_button.clicked.connect(self.add_case)  # add case event
        self.tester = tester  # 从上级窗体获得Tester()
        # case 搜索
        self.search_button = SearchButton()
        self.search_button.clicked.connect(self.update_table_data)
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.search_button)
        self.query_conditions_layout.insertWidget(5, self.tag_names_line_edit)
        # init table data
        case_list = self.db_helper.query_case_all()
        self.table_layout = TableLayout(self.tester, case_list)  # init ui table
        self.delete_case_button.clicked.connect(self.delete_case)
        self.check_button.clicked.connect(self.check_or_cancel_all)
        self.export_button.clicked.connect(self.export_data)
        self.import_button.clicked.connect(self.import_data)
        self.button_style(self.delete_case_button, '/delete.png', "Delete")
        self.button_style(self.add_case_button, '/add.png', "Add")
        self.button_style(self.import_button, '/import.png', "Import")
        self.button_style(self.export_button, '/export.png', "Export")
        self.button_style(self.check_button, '/check_all.png', "Check All")

        self.tag_list = self.db_helper.query_tag_all()
        self.set_tag_list_widget()  # show all tags
        self.set_tag_search_line()  # Set the tag input line automatic completion
        self.data_message_layout.insertWidget(1, self.table_layout)
        self.editor_widget = EditorWidget(self.tester)
        self.button_style(self.check_button, '/check_all.png', "Check All")

    def import_data(self):
        """
        import data
        :return:
        """
        file_name = QFileDialog.getOpenFileName(caption="Open File", directory="/",
                                                filter="dpk files(*.dpk)")
        if file_name[0] and '.dpk' in file_name[0]:
            conflict_tags_message_dict = self.case_data_manager.import_data(file_name[0])
            if conflict_tags_message_dict:
                self.conflict_tags_widget = ConflictTagsWidget(conflict_tags_message_dict, self.case_data_manager)
                self.conflict_tags_widget.setWindowModality(Qt.ApplicationModal)
                self.conflict_tags_widget.show()
            else:
                QMessageBox.information(self, "导入操作", "导入成功")

    def export_data(self):
        """
        export data
        :return:
        """
        self.table_layout.get_checked_data()  # todo  尝试能否直接获取到checkboxs 的状态
        if len(self.table_layout.checked_cases_message) > 0:
            path = QFileDialog.getExistingDirectory(caption="Open Directory", directory="/",
                                                    options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if path:
                case_id_list = []
                for case_message in self.table_layout.checked_cases_message:
                    case_id_list.append(case_message['case_id'])
                self.case_data_manager.export_data(path, case_id_list)
                QMessageBox.information(self, "导出操作", "导出成功")
        else:
            QMessageBox.warning(self, "导出错误", "请选择要导出的case")

    def button_style(self, button, image_path, text):
        icon = QIcon()
        config = Config()
        icon.addPixmap(QPixmap(config.images + image_path), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setText(text)
        button.setStyleSheet(
            "QPushButton{border-width:0px; background:transparent;} ")

    def check_or_cancel_all(self):
        text = self.check_button.text()
        check_status = Qt.Checked
        if text == 'Check All':
            self.check_button.setText("Cancel Check")
        else:
            self.check_button.setText("Check All")
            check_status = Qt.Unchecked
        for row in range(0, self.table_layout.dataTableWidget.rowCount()):
            check_box_item = self.table_layout.dataTableWidget.item(row, 0)
            check_box_item.setCheckState(check_status)

    def delete_case(self):
        self.table_layout.get_checked_data()  # todo  尝试能否直接获取到checkboxs 的状态
        if len(self.table_layout.checked_cases_message) > 0:
            infor_message = "确认删除" + str(len(self.table_layout.checked_cases_message)) + "条case"
            reply = QMessageBox.information(self, "删除提示", infor_message, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                for i in range(0, len(self.table_layout.checked_cases_message)):
                    case_message = self.table_layout.checked_cases_message[i]
                    self.db_helper.delete_case(int(case_message['case_id']))
                    self.table_layout.dataTableWidget.removeRow(int(case_message['row_num']) - i)  # 删除行后 行数会变 所以-i
                del self.table_layout.checked_cases_message[:]  # todo statusbar 应该提示
        else:
            QMessageBox.warning(self, "删除错误", "请选择要删除的case")

    def add_case(self):
        """
        show editor
        :return:
        """
        self.editor_widget.case_name_line_edit.setText("")
        self.editor_widget.tag_names_line_edit.setText("")
        self.editor_widget.editor_text_edit.setPlainText("")
        self.editor_widget.show()

    def update_table_data(self):
        """
        update ui table data
        :return:
        """
        self.table_layout.setParent(None)
        self.data_message_layout.removeWidget(self.table_layout)
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        case_list = []
        if tag_names != '':
            if '全部' in tag_names:
                case_list = self.db_helper.query_case_all()
            else:
                tag_names = tag_names[:len(tag_names)].split(';')
                case_list = self.db_helper.query_case_by_tag_names(tag_names)
        self.table_layout = TableLayout(self.tester, case_list)
        self.data_message_layout.insertWidget(1, self.table_layout)

    def set_tag_list_widget(self):
        """
        init ui table data and onclick event
        :return:
        """
        self.tag_list_widget.setFixedWidth(150)
        self.tag_list_widget.addItem('全部')
        for tag in self.tag_list:
            self.tag_list_widget.addItem(tag.name)
        self.tag_list_widget.itemClicked.connect(
            lambda: self.list_widget_item_clicked(self.tag_list_widget.currentItem()))

    def set_tag_search_line(self):
        """
        set tag search line
        :return:
        """
        string_list = ['全部']
        tag_names_list = string_list+self.get_tag_names()
        tag_completer = TagCompleter(tag_names_list)
        self.tag_names_line_edit.setCompleter(tag_completer)

    def get_tag_names(self):
        tag_model_list = []
        for tag in self.tag_list:
            tag_model_list.append(tag.name)
        return tag_model_list

    def list_widget_item_clicked(self, tag_list_widget_item):
        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.clear()
        self.tag_names_line_edit.setText(tag_list_widget_item.text() + ";")
        self.update_table_data()
        self.tag_names_line_edit.is_completer = True
