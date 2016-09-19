# @Time    : 2016/8/17 16:36
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from uitester.case_manager.case_data_manager import CaseDataManager
from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_search_edit import TagCompleter, TagLineEdit, SearchButton
from uitester.ui.case_manager.conflict_tag import ConflictTagsWidget
from uitester.ui.case_manager.table_widget import TableWidget
from uitester.ui.case_manager.tag_editor import TagEditorWidget


class CaseManagerWidget(QWidget):
    refresh_signal = pyqtSignal(name='refresh_data')

    def __init__(self, show_case_editor_signal, tester, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_case_editor_signal = show_case_editor_signal
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
        self.tag_names_line_edit = TagLineEdit('tag_names_line_edit', self.search_button)
        self.query_conditions_layout.insertWidget(5, self.tag_names_line_edit)
        self.table_widget = TableWidget(self.show_case_editor_signal, self.tester, [])  # init ui table

        self.delete_case_button.clicked.connect(self.delete_case)
        self.check_button.clicked.connect(self.check_or_cancel_all)
        self.export_button.clicked.connect(self.export_data)
        self.import_button.clicked.connect(self.import_data)
        self.add_tag_button.clicked.connect(self.add_tag)
        self.delete_tag_button.clicked.connect(self.delete_tag)
        self.modify_tag_button.clicked.connect(self.modify_tag)

        self.button_style(self.delete_case_button, '/delete.png', 'Delete')
        self.button_style(self.add_case_button, '/add.png', 'Add')
        self.button_style(self.import_button, '/import.png', 'Import')
        self.button_style(self.export_button, '/export.png', 'Export')
        self.button_style(self.add_tag_button, '/add.png', 'Add')
        self.button_style(self.delete_tag_button, '/delete.png', 'Delete')
        self.button_style(self.modify_tag_button, '/edit.png', 'Modify')

        self.set_tag_list_widget()  # show all tags
        self.set_tag_search_line()  # Set the tag input line automatic completion
        self.data_message_layout.insertWidget(1, self.table_widget)
        self.button_style(self.check_button, '/check_all.png', 'Check All')
        self.selected_tag_name = ''
        self.refresh_signal.connect(self.refresh, Qt.QueuedConnection)

    def check_or_cancel_all(self):
        if self.table_widget.check_all:
            check_status = Qt.Unchecked
            self.table_widget.check_all = False
        else:
            check_status = Qt.Checked
            self.table_widget.check_all = True
        for row in range(0, self.table_widget.dataTableWidget.rowCount()):
            check_box_item = self.table_widget.dataTableWidget.item(row, 0)
            check_box_item.setCheckState(check_status)

    def refresh(self):
        self.set_tag_search_line()
        self.set_tag_list_widget()

    def add_tag(self):
        '''
        add tag
        :return:
        '''
        self.tag_editor_window = TagEditorWidget(self.refresh_signal)
        self.tag_editor_window.setWindowModality(Qt.ApplicationModal)
        self.tag_editor_window.show()

    def modify_tag(self):
        items = self.tag_list_widget.selectedItems()
        item = items[0]
        if item.text() == '全部' or item.text() == '未选择':
            QMessageBox.warning(self, 'tag select ', 'tag can\'t be empty')
        else:
            self.tag_editor_window = TagEditorWidget(self.refresh_signal, item.text())
            self.tag_editor_window.setWindowModality(Qt.ApplicationModal)
            self.tag_editor_window.show()

    def delete_tag(self):
        '''
        delete tag
        :return:
        '''
        items = self.tag_list_widget.selectedItems()
        item = items[0]
        if item.text() == '全部' or item.text() == '未选择':
            QMessageBox.warning(self, 'Tag Select ', 'tag can\'t be empty')
        else:
            reply = QMessageBox.information(self, "Tag Delete", "Do you want to delete this tag?",
                                            QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:  # update case info
                self.db_helper.delete_tag_by_name(item.text())
                self.refresh_signal.emit()

    def import_data(self):
        '''
        import data
        :return:
        '''
        file_name = QFileDialog.getOpenFileName(caption='Open File', directory='/',
                                                filter='dpk files(*.dpk)')
        if file_name[0] and '.dpk' in file_name[0]:
            conflict_tags_message_dict = self.case_data_manager.import_data(file_name[0])
            if conflict_tags_message_dict:
                self.conflict_tags_widget = ConflictTagsWidget(self.refresh_signal, conflict_tags_message_dict,
                                                               self.case_data_manager)
                self.conflict_tags_widget.setWindowModality(Qt.ApplicationModal)
                self.conflict_tags_widget.show()
            else:
                QMessageBox.information(self, ' import operation', 'import success')
                self.refresh_signal.emit()

    def export_data(self):
        '''
        export data
        :return:
        '''
        self.table_widget.get_checked_data()  # todo  尝试能否直接获取到checkboxs 的状态
        if len(self.table_widget.checked_cases_message) > 0:
            path = QFileDialog.getSaveFileName(caption='Save file', directory='/',
                                               filter='dpk file(*.dpk)',
                                               options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            if path[0]:
                case_id_list = []
                for case_message in self.table_widget.checked_cases_message:
                    case_id_list.append(case_message['case_id'])
                self.case_data_manager.export_data(path[0], case_id_list)
                QMessageBox.information(self, 'export operation', 'export success')
        else:
            QMessageBox.warning(self, 'export error', 'please select a case to be exported')

    def button_style(self, button, image_path, text):
        icon = QIcon()
        config = Config()
        icon.addPixmap(QPixmap(config.images + image_path), QIcon.Normal, QIcon.Off)
        button.setIcon(icon)
        button.setText('')
        button.setToolTip(text)
        button.resize(50, 50)
        button.setStyleSheet(
            'QPushButton{border-width:0px; background:transparent;} ')

    def delete_case(self):
        self.table_widget.get_checked_data()  # todo  尝试能否直接获取到checkboxs 的状态
        if len(self.table_widget.checked_cases_message) > 0:
            infor_message = 'Confirm delete article ' + str(len(self.table_widget.checked_cases_message)) + ' case'
            reply = QMessageBox.information(self, 'delete reminder', infor_message, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                case_ids = []
                for i in range(0, len(self.table_widget.checked_cases_message)):
                    case_message = self.table_widget.checked_cases_message[i]
                    self.db_helper.delete_case(int(case_message['case_id']))
                    self.table_widget.dataTableWidget.removeRow(int(case_message['row_num']) - i)  # 删除行后 行数会变 所以-i
                    case_ids.append(int(case_message['case_id']))
                self.db_helper.batch_delete_case(case_ids)
                del self.table_widget.checked_cases_message[:]  # todo statusbar 应该提示
        else:
            QMessageBox.warning(self, 'delte error', 'please select cases to delete')

    def add_case(self):
        """
        show editor
        :return:
        """
        self.show_case_editor_signal.emit(0, 0)

    def update_table_data(self):
        '''
        update ui table data
        :return:
        '''
        self.table_widget.setParent(None)
        self.data_message_layout.removeWidget(self.table_widget)
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        case_list = []
        if tag_names != '':
            if '全部' in tag_names:
                case_list = self.db_helper.query_case_all()
            elif '未选择' in tag_names:
                case_list = self.db_helper.query_no_tag_case()
            else:
                tag_names = tag_names[:len(tag_names)].split(';')
                case_list = self.db_helper.query_case_by_tag_names(tag_names)
        self.table_widget = TableWidget(self.show_case_editor_signal, self.tester, case_list)
        self.data_message_layout.insertWidget(1, self.table_widget)

    def set_tag_list_widget(self):
        '''
        init ui table data and onclick event
        :return:
        '''
        self.tag_list_widget.clear()
        self.tag_list_widget.addItem('全部')
        self.tag_list_widget.addItem('未选择')
        self.tag_list = self.db_helper.query_tag_all()
        for tag in self.tag_list:
            self.tag_list_widget.addItem(tag.name)
        self.tag_list_widget.itemClicked.connect(
            lambda: self.list_widget_item_clicked(self.tag_list_widget.currentItem()))
        item = self.tag_list_widget.item(0)
        item.setSelected(True)
        self.list_widget_item_clicked(item)

    def set_tag_search_line(self):
        '''
        set tag search line
        :return:
        '''
        string_list = ['全部', '未选择']
        tag_names_list = string_list + self.get_tag_names()
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
        self.tag_names_line_edit.setText(tag_list_widget_item.text() + ';')
        self.update_table_data()
        self.tag_names_line_edit.is_completer = True
        self.selected_tag_name = tag_list_widget_item.text()
