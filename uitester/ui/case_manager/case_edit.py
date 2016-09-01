# @Time    : 2016/8/24 15:50
# @Author  : lixintong
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget, QListWidgetItem, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper


class CaseEdit(QMainWindow):
    def __init__(self, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_edit.ui')
        uic.loadUi(ui_file_path, self)
        self.id_line_edit.hide()
        self.db_help = DBCommandLineHelper()
        if case_id:
            self.case_id = case_id
            self.set_case_edit_data()
        self.tags_list = self.db_help.query_tag_all()
        self.set_tags_list_view()
        self.save_button.clicked.connect(self.case_save)

    def set_case_edit_data(self):
        self.case = self.db_help.query_case_by_id(self.case_id)
        self.id_line_edit.setText(self.case_id)
        self.case_name_edit.setText(self.case.name)
        self.case_content_text_edit.setPlainText(self.case.content)

    def set_tags_list_view(self):
        for tag in self.tags_list:
            item = QListWidgetItem()
            item.setText(tag.name)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if self.id_line_edit.text() and tag in self.case.tags:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.tag_list_widget.addItem(item)

    def case_save(self):
        tag_names_list = []
        for i in range(0, self.tag_list_widget.count()):
            item = self.tag_list_widget.item(i)
            if item.checkState() == Qt.Checked:
                tag_names_list.append(item.text())
        case_id = self.id_line_edit.text()
        case_name = self.case_name_edit.text()
        case_content = self.case_content_text_edit.toPlainText()
        add_tag_names = self.add_tag_names.text()

        if case_name=='' or case_content=='' or (add_tag_names == '' and len(tag_names_list) == 0):
            QMessageBox.warning(self, "操作错误", "信息不全，请检查")
            return
        if '；' in add_tag_names:
            QMessageBox.warning(self, "操作错误", "添加标签含有中文符号‘；’")
            return
        if add_tag_names:
            if add_tag_names[len(add_tag_names) - 1:len(add_tag_names)] == ';':
                add_tag_names = add_tag_names[:len(add_tag_names) - 1]
            add_tag_names = add_tag_names.split(';')
        if case_id:
            self.db_help.update_case(case_id, case_name, case_content, tag_names_list, add_tag_names)
            QMessageBox.information(self, "修改操作", "修改成功")
        else:
            case = self.db_help.insert_case_with_tagnames(case_name, case_content, tag_names_list, add_tag_names)
            self.id_line_edit.setText(str(case.id))
            QMessageBox.information(self, "添加操作", "添加成功")  # todo 添加定时器 QTimer
