# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_manager.case_text_edit import TextEdit, Completer
from uitester.ui.case_manager.highlighter import MyHighlighter
from uitester.ui.case_run.add_device import AddDeviceWidget
from uitester.ui.case_run.tag_names_line_edit import TagLineEdit, TagCompleter


class EditorWidget(QWidget):
    device_list_signal = pyqtSignal(list, list)

    def __init__(self, tester, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_editor.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        self.id_line_edit.hide()   # 隐藏line_edit

        # set icon
        save_icon = QIcon()
        config = Config()
        save_icon.addPixmap(QPixmap(config.images + '/save.png'), QIcon.Normal, QIcon.Off)
        self.save_btn.setIcon(save_icon)

        # set icon
        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_btn.setIcon(run_icon)

        self.message_box = QMessageBox()
        self.high_lighter = None

        self.case_name_line_edit.setPlaceholderText("Case Name")   # 设置提示文字

        # tag name 输入框
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit")
        self.tag_list = None
        self.tag_names_line_edit_adapter()

        self.tester = tester   # 从上级窗体拿到tester()
        self._kw_core = self.tester.get_kw_runner()

        self.editor_text_edit = TextEdit(self.tester)  # case content编辑框
        self.editor_layout.insertWidget(0, self.editor_text_edit)
        self.editor_adapter()

        self.add_devices_widget = AddDeviceWidget()  # add device
        self.add_devices_widget.setWindowModality(Qt.WindowModal)  # 设置模态
        self.device_list_signal.connect(self.add_devices_widget.add_radio_to_widget, Qt.QueuedConnection)

        self.save_btn.clicked.connect(self.save_event)
        self.run_btn.clicked.connect(self.run_event)

        self.parsed_line_list = []  # 存放解析后的kw

        self.case_id = case_id
        self.set_case_edit_data()

    def set_case_edit_data(self):
        """
        编辑case，设置原始数据
        :return:
        """
        if self.case_id:
            case = self.dBCommandLineHelper.query_case_by_id(self.case_id)
            self.id_line_edit.setText(self.case_id)
            self.case_name_line_edit.setText(case.name)
            tags = ''
            for tag in case.tags:
                tags = tags + tag.name + ";"
            self.tag_names_line_edit.setText(tags)
            self.editor_text_edit.setPlainText(case.content)

    def save_event(self):
        case_name = self.case_name_line_edit.text().strip()  # Case Name
        content = self.editor_text_edit.toPlainText().strip()  # Case Content
        is_null = self.check_null()
        if is_null:
            return
        tag_names = self.tag_names_line_edit.text().split(";")
        # 去除list中的空值
        for tag in tag_names:
            if not tag:
                tag_names.remove(tag)

        if self.case_id:
            self.dBCommandLineHelper.update_case(self.case_id, case_name, content, tag_names)
            self.message_box.information(self, "Update case", "Update case success.", QMessageBox.Ok)
        else:
            case = self.dBCommandLineHelper.insert_case_with_tagnames(case_name, content, tag_names)
            self.id_line_edit.setText(str(case.id))
            self.message_box.information(self, "Add case", "Add case success.", QMessageBox.Ok)

        self.close()

    def run_event(self):
        if self.check_null():
            return
        # TODO 选device 获得Tester devices
        self.device_list_signal.emit([], [111])
        self.add_devices_widget.show()

    def check_null(self):
        """
        检查必填项是否为空
        :return:
        """
        is_none = False
        type_info = ''
        case_name = self.case_name_line_edit.text().strip()
        content = self.editor_text_edit.toPlainText().strip()

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
            self.message_box.warning(self, "Message", type_info + " is required.", QMessageBox.Ok)
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
        kw_core = self.tester.get_kw_runner()
        func_dict = kw_core.user_func    # 获取默认func
        cmp = Completer(func_dict)
        self.editor_text_edit.set_completer(cmp)

        # 高亮显示
        self.high_lighter = MyHighlighter(self.editor_text_edit)



