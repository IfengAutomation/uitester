# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_text_edit import TextEdit, Completer
from uitester.ui.case_manager.highlighter import MyHighlighter
from uitester.ui.case_manager.tag_names_line_edit import TagLineEdit, TagCompleter


class EditorWidget(QWidget):

    def __init__(self, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_editor.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        self.id_line_edit.hide()   # 隐藏line_edit

        if case_id:
            self.case_id = case_id

        # set icon
        save_icon = QIcon()
        config = Config()
        save_icon.addPixmap(QPixmap(config.images + '/save.png'), QIcon.Normal, QIcon.Off)
        self.save_btn.setIcon(save_icon)

        # set icon
        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_btn.setIcon(run_icon)

        self.case_name_line_edit.setPlaceholderText("Case Name")   # 设置提示文字

        # tag name 输入框
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit")
        self.tag_list = None
        self.tag_names_line_edit_adapter()

        self.editor_text_edit = TextEdit()
        self.editor_layout.insertWidget(0, self.editor_text_edit)
        self.editor_adapter()

        self.save_btn.clicked.connect(self.save_event)

    def save_event(self):
        case_name = self.case_name_line_edit.text().strip()
        content = self.editor_text_edit.toPlainText().strip()
        is_null = self.check_null(case_name, content)
        if is_null:
            return
        tag_names = self.tag_names_line_edit.text().split(";")   # TODO 可为空，list
        # 去除list中的空值
        for tag in tag_names:
            if not tag:
                tag_names.remove(tag)
        # TODO 存入库
        # DBCommandLineHelper.insert_case(case_name, content, tag_names)
        self.close()

    def check_null(self, case_name, content):
        """
        检查必填项是否为空
        :return:
        """
        is_none = False
        type_info = ''

        if not case_name:
            is_none = True
            type_info += "Case Name"
        if not content:
            is_none = True
            if not type_info:
                type_info += "Content"
            else:
                type_info += ", Content"
        if is_none:
            QMessageBox.about(self, "Message", type_info + " is required.")
        return is_none

    def tag_names_line_edit_adapter(self):
        """
        给tag_names_line_edit设置自动提示、默认显示提示文字等
        :return:
        """
        self.tag_names_line_edit.setPlaceholderText("Tag Names")   # 设置提示文字
        self.tag_layout.insertWidget(0, self.tag_names_line_edit)

        self.tag_list = self.dBCommandLineHelper.query_tag_all()  # 获取所有tag
        tag_name_list = []
        for tag in self.tag_list:
            tag_name_list.append(tag.name)
        cmp = TagCompleter(tag_name_list)
        self.tag_names_line_edit.setCompleter(cmp)

    def editor_adapter(self):
        # TODO for test， 获取 keyword， 给以提示
        li = ['The', 'that', 'this', 'Red', 'right', 'what']
        # 自动提示
        cmp = Completer(li)
        self.editor_text_edit.set_completer(cmp)

        # 高亮显示
        MyHighlighter(self.editor_text_edit)


