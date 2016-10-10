# @Time    : 2016/9/26 18:06
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QMenu, QAction

from uitester.case_data_manager.case_data_manager import CaseDataManager
from uitester.case_manager.database import CaseData


class CaseDataWidget(QWidget):
    refresh_table_item_signal = pyqtSignal(int, int, str, name='refresh_table_item')

    def __init__(self, case_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_data.ui')
        uic.loadUi(ui_file_path, self)
        self.case_id = case_id
        self.case_data_service = CaseDataManager()
        self.create_menu()
        self.set_table_widget()
        self.refresh_table_item_signal.connect(self.refresh_table_item, Qt.QueuedConnection)
        self.message_box = QMessageBox()
        self.delete_data_ids = []
        self.del_column_num = -1

    def create_menu(self):
        self.pop_menu = QMenu()
        delete_action = QAction("Delete Column", self.pop_menu)
        delete_action.triggered.connect(lambda: self.del_column(self.del_column_num))
        self.pop_menu.addAction(delete_action)

    def del_column(self, column):
        if column != -1:  # 非初始
            for case_data in self.case_data_list[1:]:
                case_data_detail = case_data[column]
                if case_data_detail.id:
                    self.delete_data_ids.append(case_data_detail.id)
                case_data[column] = CaseData()
            for case_data in self.case_data_list:
                del case_data[column]
            self.table_widget.removeColumn(column)
            column = -1
        else:
            pass

    def set_table_widget(self):
        self.row_count = 30
        self.column_count = 30
        self.case_data_list = self.case_data_service.get_format_case_data(self.row_count, self.column_count,
                                                                          self.case_id)
        self.table_widget.setRowCount(self.row_count)
        self.table_widget.setColumnCount(self.column_count)
        for row in range(0, self.row_count):
            for column in range(0, self.column_count):
                case_data_detail = self.case_data_list[row][column]
                if type(self.case_data_list[row][column]) == CaseData:
                    self.table_widget.setItem(row, column,
                                              QTableWidgetItem(case_data_detail.data))
                else:
                    self.table_widget.setItem(row, column,
                                              QTableWidgetItem(case_data_detail))
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.cellClicked.connect(self.table_widget_clicked)
        self.table_widget.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.horizontalHeader().customContextMenuRequested.connect(self.show_contextmenu)

    def show_contextmenu(self, pos):
        self.del_column_num = self.table_widget.horizontalHeader().logicalIndexAt(pos)

        self.pop_menu.exec(QCursor.pos())

    def table_widget_clicked(self, row, column):
        table_item = self.table_widget.item(row, column)
        if row == 0:  # 修改字段名
            self.data_header_editor = DataHeaderQWidget(self.refresh_table_item_signal,
                                                        row, column, table_item.text())
            self.data_header_editor.show()
        else:  # 修改数据
            self.data_editor = DataEditorQWidget(self.refresh_table_item_signal,
                                                 row, column, table_item.text())
            self.data_editor.show()

    def refresh_table_item(self, row, column, text):
        table_item = self.table_widget.item(row, column)
        table_item.setText(text)
        case_data_detail = self.case_data_list[row][column]
        if type(case_data_detail) == CaseData:
            case_data_detail.data = text
        else:
            self.case_data_list[row][column] = text


class DataHeaderQWidget(QWidget):
    def __init__(self, refresh_table_item_signal, row, column,
                 old_header_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'header_editor.ui')
        uic.loadUi(ui_file_path, self)
        self.new_name_line_edit.setText(old_header_name)
        self.save_btn.clicked.connect(self.save_data_header)
        self.message_box = QMessageBox()
        self.refresh_table_item_signal = refresh_table_item_signal
        self.row = row
        self.column = column

    def save_data_header(self):
        new_header_name = self.new_name_line_edit.text()
        new_header_name = new_header_name.strip()
        self.refresh_table_item_signal.emit(self.row, self.column, new_header_name)
        self.close()

class DataEditorQWidget(QWidget):
    def __init__(self, refresh_table_item_signal, row, column,
                 old_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'data_editor.ui')
        uic.loadUi(ui_file_path, self)
        self.data_text_edit.setPlainText(old_data)
        self.save_btn.clicked.connect(self.save_data)
        self.refresh_table_item_signal = refresh_table_item_signal
        self.row = row
        self.column = column

    def save_data(self):
        new_data = self.data_text_edit.toPlainText().strip()
        self.refresh_table_item_signal.emit(self.row, self.column, new_data)
        self.close()
