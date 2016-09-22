# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QSplitter

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter, SearchButton
from uitester.ui.case_manager.case_text_edit import TextEdit, Completer
from uitester.ui.case_manager.highlighter import MyHighlighter
from uitester.ui.case_manager.tag_manage_widget import TagManageWidget
from uitester.ui.case_run.add_device import AddDeviceWidget
from uitester.ui.case_run.console import Console


class EditorWidget(QWidget):
    device_list_signal = pyqtSignal(list, name="device_list_signal")
    import_list_signal = pyqtSignal(set, name="import_list_signal")

    def __init__(self, refresh_signal, tester, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_editor.ui')
        uic.loadUi(ui_file_path, self)

        self.dBCommandLineHelper = DBCommandLineHelper()
        self.tester = tester
        self.config = self.tester.get_config()
        self.kw_core = self.tester.get_kw_runner()
        self.case_id = case_id
        self.refresh_signal = refresh_signal

        self.init_ui()

        self.is_log_show = True
        self.is_running = False
        self.tag_list = []
        self.parsed_line_list = []
        self.case = None
        self.high_lighter = None
        self.tag_manage_widget = None
        self.add_device_widget = None

        self.message_box = QMessageBox()
        self.add_tag_button = SearchButton()
        self.tag_names_line_edit = TagLineEdit("tag_names_line_edit", self.add_tag_button)
        self.set_tag_name_completer()

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setHandleWidth(1)   # set handle width
        self.editor_text_edit = TextEdit(self.kw_core)  # case content TextEdit
        self.console = Console()

        # Add the 'editor text edit' and 'console' to splitter
        self.splitter.addWidget(self.editor_text_edit)
        self.splitter.addWidget(self.console)

        # Set the initial scale: 4:1
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 1)

        self.editor_layout.addWidget(self.splitter)

        self.editor_adapter()  # set completer and highlighter
        self.set_case_edit_data()  # update case

        self.import_list_signal.connect(self.editor_text_edit.get_import_from_content, Qt.QueuedConnection)
        self.editor_text_edit.parse_error_info_signal.connect(self.add_error_info, Qt.QueuedConnection)

        # button event
        self.save_btn.clicked.connect(self.save_case)
        self.run_btn.clicked.connect(self.run_btn_event)
        self.console_btn.clicked.connect(self.log_show_hide_event)
        self.add_tag_button.clicked.connect(self.choose_event)

    def init_ui(self):
        """
        init ui, include: resize window
        :return:
        """
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.init_btn_icon()

        self.id_line_edit.hide()  # hide line_edit
        self.case_name_line_edit.setPlaceholderText("Case Name")

    def init_btn_icon(self):
        """
        init button icon, including: save button、run button、show/hide console button
        :return:
        """
        save_icon = QIcon()
        save_icon.addPixmap(QPixmap(self.config.images + '/save.png'), QIcon.Normal, QIcon.Off)           # save icon
        self.save_btn.setIcon(save_icon)

        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)             # run icon
        self.run_btn.setIcon(run_icon)

        console_icon = QIcon()
        console_icon.addPixmap(QPixmap(self.config.images + '/console.png'), QIcon.Normal, QIcon.Off)     # console icon
        self.console_btn.setIcon(console_icon)

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
        original_tag_names = self.tag_names_line_edit.text().strip()
        tag_name_set = set(original_tag_names.split(";"))  # original tag name set
        if not tag_names:
            return
        # handle the repeat tag names
        tag_name_list = tag_names.split(";")
        for tag_name in tag_name_list:
            if (tag_name.strip() in original_tag_names) or (not tag_name.strip()):
                continue
            tag_name_set.add(tag_name.strip())  # add new selected tag name
        all_tag_names = ""
        for tag_name in tag_name_set:
            if not tag_name.strip():
                continue
            all_tag_names += tag_name.strip() + ";"

        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.setText(all_tag_names)
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
        append error massage to console
        :param info:
        :return:
        """
        self.console.append("<font color='red'>" + info + "</font>")

    def set_case_edit_data(self):
        """
        init data for update case
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

            init_import_list = set()
            for cmd in self.case.content.split("\n"):
                if cmd.strip().find("import") == 0:
                    init_import_list.add(cmd.strip())
            self.import_list_signal.emit(init_import_list)

    def closeEvent(self, event):
        """
        close window event
        :param event:
        :return:
        """
        case_name = self.case_name_line_edit.text().strip()  # Case Name
        content = self.editor_text_edit.toPlainText().strip()  # Case Content
        tag_list = self.get_tag_list()
        if not self.case_id:
            if (not case_name) and (not content) and (not tag_list):
                self.close()
                return
        else:
            if not self.check_modify():
                self.close()
                return
        self.handle_message_box_apply(event)

    def handle_message_box_apply(self, event):
        """
        message box
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
        check the changes of the case
        :return:
        """
        is_case_modified = False
        case_db = self.dBCommandLineHelper.query_case_by_id(self.case_id)

        is_name_modified = case_db.name.strip() != self.case_name_line_edit.text().strip()
        is_content_modified = case_db.content.strip() != self.editor_text_edit.toPlainText().strip()

        # tag names in the line edit
        tag_list = self.get_tag_list()
        # tag names in db
        db_tag_list = case_db.tags
        is_tags_names_modify = list(set(db_tag_list).difference(set(tag_list))) != list(set(tag_list).difference(set(db_tag_list)))

        if is_name_modified or is_content_modified or is_tags_names_modify:
            is_case_modified = True
        return is_case_modified

    def get_tag_list(self):
        """
        get tag list from tag_names_line_edit
        :return:
        """
        # get tag names
        tag_name_list = self.tag_names_line_edit.text().strip().split(";")
        tag_set = set()
        for tag_name in tag_name_list:
            if not tag_name.strip():
                continue
            tag = self.dBCommandLineHelper.query_tag_by_name(tag_name.strip())
            tag_set.add(tag)
        return list(tag_set)

    def run_btn_event(self):
        """
        click run button, show add_device_widget
        :return:
        """
        self.add_device_widget = AddDeviceWidget()  # add device
        self.add_device_widget.setWindowModality(Qt.WindowModal)
        self.device_list_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.add_device_widget.run_signal.connect(self.run_case, Qt.QueuedConnection)
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
        try:
            self.tester.stop()
            self.tester.stop_server()
        except Exception as e:
            self.add_error_info(str(e))

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
            try:
                self.kw_core.parse_line(kw)
            except Exception as e:
                self.add_error_info(str(e))
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
        if self.check_null():
            if event:
                event.ignore()
            return
        tags = self.get_tag_list()

        if self.check_tag_name():   # check unrecognized tag names
            return

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
        check the required options
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
        get keywords for the completer and the highlighter
        :return:
        """
        if self.case_id:
            self.parse_import()

        func_dict = self.kw_core.user_func  # get default functions
        cmp = Completer(func_dict)
        self.editor_text_edit.set_completer(cmp)

        # highlighter
        kw_list = []
        for func_name, func in func_dict.items():
            kw_list.append(func_name)
        self.high_lighter = MyHighlighter(self.editor_text_edit, kw_list)
        self.editor_text_edit.set_highlighter(self.high_lighter)

    def parse_import(self):
        """
        parse all the 'import' block in the case content
        :return:
        """
        import_list = set()
        content_list = self.dBCommandLineHelper.query_case_by_id(self.case_id).content.split("\n")
        if not content_list:
            return
        for line in content_list:
            if line.strip().find("import") == 0:
                import_list.add(line.strip())

        self.kw_core.user_func.clear()
        self.kw_core.user_func = {**self.kw_core.default_func}
        for import_cmd in import_list:
            try:
                self.kw_core.parse_line(import_cmd)
            except Exception as e:
                self.add_error_info(str(e))

    def set_tag_name_completer(self):
        """
        set completer to tag_names_line_edit
        :return:
        """
        # change button icon
        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(self.config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.add_tag_button.setIcon(add_icon)

        self.tag_names_line_edit.setPlaceholderText("Tag Names")
        self.tag_layout.insertWidget(0, self.tag_names_line_edit)

        self.tag_list = self.dBCommandLineHelper.query_tag_all()  # get all tags
        tag_name_list = []
        for tag in self.tag_list:
            tag_name_list.append(tag.name)
        cmp = TagCompleter(tag_name_list)
        self.tag_names_line_edit.setCompleter(cmp)

    def check_tag_name(self):
        """
        check tag name,return unrecognized tag names
        :return:
        """
        tag_name_list = self.tag_names_line_edit.text().strip().split(";")
        unrecognized_tag_names = ""
        has_unrecognized = False
        for tag_name in tag_name_list:
            if not tag_name.strip():
                continue
            tag = self.dBCommandLineHelper.query_tag_by_name(tag_name.strip())
            if not tag:
                unrecognized_tag_names += "\"" + tag_name + "\"" + "、"
        if not unrecognized_tag_names:
            return has_unrecognized
        has_unrecognized = True
        unrecognized_tag_names = unrecognized_tag_names[:-1]
        self.message_box.about(self, "Warning", "Tag name: " + unrecognized_tag_names +
                               " unrecognized, please add it first.")
        return has_unrecognized



