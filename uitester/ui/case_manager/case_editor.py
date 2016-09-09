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
    import_list_signal = pyqtSignal(set)

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

        # set icon
        console_icon = QIcon()
        console_icon.addPixmap(QPixmap(config.images + '/console.png'), QIcon.Normal, QIcon.Off)
        self.console_btn.setIcon(console_icon)

        self.message_box = QMessageBox()
        self.high_lighter = None

        self.case_name_line_edit.setPlaceholderText("Case Name")   # 设置提示文字

        # tag name 输入框
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit")
        self.tag_list = None
        self.tag_names_line_edit_adapter()

        self.tester = tester   # 从上级窗体拿到tester()
        self.kw_core = self.tester.get_kw_runner()
        self.config = self.tester.get_config()

        self.case_id = case_id

        self.editor_text_edit = TextEdit(self.kw_core)  # case content编辑框
        self.editor_layout.insertWidget(0, self.editor_text_edit)
        self.editor_adapter()
        self.console.hide()  # 隐藏log提示框

        self.add_devices_widget = AddDeviceWidget()  # add device
        self.add_devices_widget.setWindowModality(Qt.WindowModal)  # 设置模态
        self.device_list_signal.connect(self.add_devices_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.import_list_signal.connect(self.editor_text_edit.get_import_from_content, Qt.QueuedConnection)

        self.is_log_show = False
        # button event
        self.save_btn.clicked.connect(self.save_event)
        self.run_btn.clicked.connect(self.run_event)
        self.console_btn.clicked.connect(self.log_show_hide_event)

        self.parsed_line_list = []  # 存放解析后的kw

        self.set_case_edit_data()

    def log_show_hide_event(self):
        if self.is_log_show:
            self.console_btn.setText("Show Console")
            self.console.hide()
            self.is_log_show = False
        else:
            self.console_btn.setText("Hide Console")
            self.console.show()
            self.is_log_show = True

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

            # 获取case content中import语句list，发送到text_edit中
            init_import_list = set()
            for cmd in case.content.split("\n"):
                if cmd.strip().find("import") == 0:
                    init_import_list.add(cmd.strip())
            self.import_list_signal.emit(init_import_list)

    def closeEvent(self, event):
        """
        窗体关闭时触发事件，判断case 是否有更改，提示保存或放弃保存
        :param event:
        :return:
        """
        case_name = self.case_name_line_edit.text().strip()  # Case Name
        content = self.editor_text_edit.toPlainText().strip()  # Case Content
        tag_name_list = self.get_tag_name_list()
        if not self.case_id:
            if (not case_name) and (not content) and (not tag_name_list):
                # add case，没有输入有效内容时直接关闭
                self.close()
                return
        else:
            if not self.check_modify():
                self.close()
                return
        self.handle_message_box_apply(event)

    def handle_message_box_apply(self, event):
        """
        处理关闭对话框
        :param event:
        :return:
        """
        reply = self.message_box.question(self, "Case Editor", "Do you want to save this case?",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if reply == QMessageBox.Yes:  # update case info
            self.save_case(event)
        elif reply == QMessageBox.No:
            self.close()
            return
        else:
            event.ignore()

    def check_modify(self):
        """
        判断case信息是否有改动
        :return:
        """
        is_case_modified = False
        case = self.dBCommandLineHelper.query_case_by_id(self.case_id)

        is_name_modified = case.name != self.case_name_line_edit.text().strip()
        is_content_modified = case.content != self.editor_text_edit.toPlainText().strip()

        # 处理页面中tag names
        tag_name_list = self.get_tag_name_list()
        # 处理库中tag names
        db_tag_name_list = []
        for db_tag in case.tags:
            db_tag_name_list.append(db_tag.name)
        is_tags_names_modify = db_tag_name_list != tag_name_list

        if is_name_modified or is_content_modified or is_tags_names_modify:
            is_case_modified = True
        return is_case_modified

    def get_tag_name_list(self):
        """
        将tag names输入框中内容转换为tag name list
        :return:
        """
        # 处理页面中tag names
        tag_name_list = self.tag_names_line_edit.text().strip().split(";")
        # 去除list中的空值
        for tag in tag_name_list:
            if not tag:
                tag_name_list.remove(tag)
        return tag_name_list

    def save_event(self):
        self.save_case()

    def run_event(self):
        if self.check_null():
            return
        # TODO 选device 获得Tester devices
        self.device_list_signal.emit([], [111])
        self.add_devices_widget.show()

    def save_case(self, event=None):
        """
        保存case
        :return:
        """
        case_name = self.case_name_line_edit.text().strip()  # Case Name
        content = self.editor_text_edit.toPlainText().strip()  # Case Content
        is_null = self.check_null()
        if is_null:
            if event:  # close event 只关闭参数不能为空提示框，不关闭编辑框
                event.ignore()
            return
        tag_names = self.get_tag_name_list()

        if self.case_id:
            self.dBCommandLineHelper.update_case(self.case_id, case_name, content, tag_names)
            self.message_box.information(self, "Update case", "Update case success.", QMessageBox.Ok)
        else:
            case = self.dBCommandLineHelper.insert_case_with_tagnames(case_name, content, tag_names)
            self.id_line_edit.setText(str(case.id))
            self.case_id = self.id_line_edit.text().strip()
            self.message_box.information(self, "Add case", "Add case success.", QMessageBox.Ok)

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
        """
        获取keyword，给以提示
        :return:
        """
        if self.case_id:
            self.parse_import()

        func_dict = self.kw_core.user_func  # 获取默认func
        cmp = Completer(func_dict)
        self.editor_text_edit.set_completer(cmp)

        # 高亮显示
        kw_list = []
        for func_name, func in func_dict.items():
            kw_list.append(func_name)
        self.high_lighter = MyHighlighter(self.editor_text_edit, kw_list)
        self.editor_text_edit.set_highlighter(self.high_lighter)

    def parse_import(self):
        """
        遍历case content，解析import语句
        :return:
        """
        import_list = set()
        content_list = self.dBCommandLineHelper.query_case_by_id(self.case_id).content.split("\n")
        if not content_list:
            return
        for line in content_list:
            if line.strip().find("import") == 0:
                import_list.add(line.strip())
        # 重置
        self.kw_core.user_func.clear()
        self.kw_core.user_func = {**self.kw_core.default_func}
        for import_cmd in import_list:
            self.kw_core.parse_line(import_cmd)




