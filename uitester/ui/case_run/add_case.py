# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter, SearchButton
from uitester.ui.case_run.table_widget import RunnerTableWidget


class AddCaseWidget(QWidget):
    select_case_signal = pyqtSignal(list, name="select_case_signal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_case.ui')
        uic.loadUi(ui_file_path, self)

        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        self.search_button = SearchButton()
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.search_button)
        self.tag_names_line_edit_adapter()
        self.tag_list = None

        self.result_widget = RunnerTableWidget(self.dBCommandLineHelper.query_case_all(), [])
        self.result_table_layout.insertWidget(0, self.result_widget)

        self.message_box = QMessageBox()

        self.search_button.clicked.connect(self.search_event)
        self.selectcasebtn.clicked.connect(self.select_event)
        self.casecancelbtn.clicked.connect(self.close)

    def search_event(self):
        """
        search tags by tag name, and show the result in the table widget
        :return:
        """
        self.result_widget.setParent(None)
        self.result_table_layout.removeWidget(self.result_widget)
        tag_names = self.tag_names_line_edit.text()
        tag_names = tag_names[0: len(tag_names) - 1]
        case_list = []
        if tag_names != '':
            tag_names = tag_names[:len(tag_names)].split(';')
            case_list = self.dBCommandLineHelper.query_case_by_tag_names(tag_names)
        else:
            case_list = self.db_helper.query_case_all()
        self.result_widget = RunnerTableWidget(case_list, [])
        self.result_table_layout.insertWidget(0, self.result_widget)

    def select_event(self):
        """
        handle the select event
        :return:
        """
        self.result_widget.get_checked_data()
        if not self.result_widget.checked_cases_message:
            self.message_box.warning(self, "Message", "Please choose cases first.", QMessageBox.Ok)
            return
        id_list = []
        for item in self.result_widget.checked_cases_message:
            id_list.append(int(item["case_id"]))
        self.select_case_signal.emit(id_list)
        self.close()     # close AddCase

    def tag_names_line_edit_adapter(self):
        """
        settings for tag_names_line_edit
        such as completer, placeholder text
        :return:
        """
        self.tag_names_line_edit.setPlaceholderText("Tag names")
        self.search_layout.insertWidget(0, self.tag_names_line_edit)

        self.tag_list = self.dBCommandLineHelper.query_tag_all()  # get all tags
        tag_name_list = []
        for tag in self.tag_list:
            tag_name_list.append(tag.name)
        cmp = TagCompleter(tag_name_list)
        self.tag_names_line_edit.setCompleter(cmp)
