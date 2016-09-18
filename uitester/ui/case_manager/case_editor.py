# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter
from uitester.ui.case_manager.case_text_edit import TextEdit, Completer
from uitester.ui.case_manager.highlighter import MyHighlighter
from uitester.ui.case_manager.tag_manage_button import ChooseButton
from uitester.ui.case_manager.tag_manage_widget import TagManageWidget
from uitester.ui.case_run.add_device import AddDeviceWidget


class EditorWidget(QWidget):
    device_list_signal = pyqtSignal(list)
    import_list_signal = pyqtSignal(set)

    def __init__(self, refresh_signal, tester, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dBCommandLineHelper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_editor.ui')
        uic.loadUi(ui_file_path, self)

        self.tester = tester

        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        self.id_line_edit.hide()   # hide line_edit

        # set icon
        save_icon = QIcon()
        config = self.tester.get_config()
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

        self.kw_core = self.tester.get_kw_runner()
        self.config = self.tester.get_config()

        self.case_id = case_id

        # tag name 输入框
        self.tag_list = []
        self.choose_button = ChooseButton()
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.choose_button)
        self.tag_names_line_edit.setReadOnly(True)
        self.tag_layout.insertWidget(0, self.tag_names_line_edit)

        self.editor_text_edit = TextEdit(self.kw_core)  # case content TextEdit
        self.editor_layout.insertWidget(0, self.editor_text_edit)
        self.editor_adapter()
        self.console.hide()  # hide log

        self.add_device_widget = AddDeviceWidget()  # add device
        self.add_device_widget.setWindowModality(Qt.WindowModal)
        self.device_list_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.import_list_signal.connect(self.editor_text_edit.get_import_from_content, Qt.QueuedConnection)
        self.editor_text_edit.parse_error_info_signal.connect(self.add_error_info, Qt.QueuedConnection)
        self.add_device_widget.run_signal.connect(self.run_case, Qt.QueuedConnection)

        self.tag_manage_widget = None

        self.is_log_show = False
        # button event
        self.save_btn.clicked.connect(self.save_case)
        self.run_btn.clicked.connect(self.run_event)
        self.console_btn.clicked.connect(self.log_show_hide_event)
        self.choose_button.clicked.connect(self.choose_event)

        self.parsed_line_list = []
        self.case = None
        self.set_case_edit_data()
        self.refresh_signal = refresh_signal
        self.is_running = False

    def choose_event(self):
        """
        choose tag event, show tags
        :return:
        """
        self.tag_manage_widget = TagManageWidget(self.config)
        self.tag_manage_widget.selected_tag_names_signal.connect(self.set_selected_tag_names)
        self.tag_manage_widget.setWindowModality(Qt.ApplicationModal)
        self.tag_manage_widget.show()

    def set_selected_tag_names(self, tag_names):
        """
        set tag names
        :param tag_names:
        :return:
        """
        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.setText(tag_names)
        self.tag_names_line_edit.is_completer = True

    def log_show_hide_event(self):
        if self.is_log_show:
            self.console_btn.setText("Show Console")
            self.console.hide()
            self.is_log_show = False
        else:
            self.console_btn.setText("Hide Console")
            self.console.show()
            self.is_log_show = True

    def add_error_info(self, info):
        """
        添加error信息到console中
        :param info:
        :return:
        """
        self.console.append("<font color='red'>" + info + "</font>")

    def set_case_edit_data(self):
        """
        编辑case，设置原始数据
        :return:
        """
        if self.case_id:
            self.case = self.dBCommandLineHelper.query_case_by_id(self.case_id)
            self.id_line_edit.setText(self.case_id)
            self.case_name_line_edit.setText(self.case.name)
            tags = ''
            for tag in self.case.tags:
                tags = tags + tag.name + ";"
            self.tag_names_line_edit.setText(tags)
            self.editor_text_edit.setPlainText(self.case.content)

            # 获取case content中import语句list，发送到text_edit中
            init_import_list = set()
            for cmd in self.case.content.split("\n"):
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
        tag_list = self.get_tag_list()
        if not self.case_id:
            if (not case_name) and (not content) and (not tag_list):
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
        case_db = self.dBCommandLineHelper.query_case_by_id(self.case_id)

        is_name_modified = case_db.name.strip() != self.case_name_line_edit.text().strip()
        is_content_modified = case_db.content.strip() != self.editor_text_edit.toPlainText().strip()

        # 处理页面中tag names
        tag_list = self.get_tag_list()
        # 处理库中tag names
        db_tag_list = case_db.tags
        is_tags_names_modify = db_tag_list != tag_list

        if is_name_modified or is_content_modified or is_tags_names_modify:
            is_case_modified = True
        return is_case_modified

    def get_tag_list(self):
        """
        将tag names输入框中内容转换为tag name list
        :return:
        """
        # 处理页面中tag names
        tag_name_list = self.tag_names_line_edit.text().strip().split(";")
        tag_list = []
        # 去除list中的空值
        for tag_name in tag_name_list:
            if tag_name:
                tag = self.dBCommandLineHelper.query_tag_by_name(tag_name)
                tag_list.append(tag)
        return tag_list

    def run_event(self):
        devices = []
        if self.check_null():
            return
        if self.is_running:
            self.stop_case()
            return
        if self.tester.devices():
            devices = self.tester.devices()
        self.device_list_signal.emit(devices)
        self.add_device_widget.show()

    def run_case(self, devices):
        # change icon
        stop_icon = QIcon()
        stop_icon.addPixmap(QPixmap(self.config.images + '/stop.png'), QIcon.Normal, QIcon.Off)
        self.run_btn.setIcon(stop_icon)
        self.run_btn.setText("Stop")
        self.is_running = True
        if not devices:
            return
        self.tester.select_devices(devices)
        self.run()   # run

    def stop_case(self):
        # set icon
        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_btn.setIcon(run_icon)
        self.run_btn.setText("Run")
        self.is_running = False
        # TODO 停止执行
        self.tester.stop()
        self.tester.stop_server()

    def run(self):
        """
        run case content
        :return:
        """
        self.tester.start_server()
        case_content = self.editor_text_edit.toPlainText().strip()
        kw_list = case_content.split("\n")
        self.kw_core.parsed_line = []
        for kw in kw_list:
            self.kw_core.parse_line(kw)
        try:
            self.kw_core.execute()
        except Exception as e:
            self.stop_case()
            self.add_error_info(str(e))
        self.stop_case()

    def save_case(self, event=None):
        """
        save case
        :return:
        """
        case_name = self.case_name_line_edit.text().strip()  # Case Name
        content = self.editor_text_edit.toPlainText()  # Case Content
        is_null = self.check_null()
        if is_null:
            if event:  # close event 只关闭参数不能为空提示框，不关闭编辑框
                event.ignore()
            return
        tags = self.get_tag_list()
        # TODO check new tag

        if self.case_id:
            self.case.name = case_name
            self.case.content = content
            self.case.tags = tags
            self.dBCommandLineHelper.update_case()
            self.message_box.information(self, "Update case", "Update case success.", QMessageBox.Ok)
        else:
            case = self.dBCommandLineHelper.insert_case_with_tags(case_name, content, tags)
            self.id_line_edit.setText(str(case.id))
            self.case_id = self.id_line_edit.text().strip()
            self.set_case_edit_data()
            self.message_box.information(self, "Add case", "Add case success.", QMessageBox.Ok)
        self.refresh_signal.emit()

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




