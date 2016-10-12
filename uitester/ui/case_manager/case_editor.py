# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QSplitter

from uitester.case_data_manager.case_data_manager import CaseDataManager
from uitester.case_manager.case_manager import CaseManager
from uitester.case_manager.database import DBCommandLineHelper

from uitester.test_manager import rpc_agent
from uitester.ui.case_data.case_data import CaseDataWidget
from uitester.ui.case_manager.case_editor_run_status_listener import EditorRunStatusListener
from uitester.ui.case_manager.case_search_edit import TagLineEdit, TagCompleter, SearchButton
from uitester.ui.case_manager.case_text_edit import TextEdit, Completer
from uitester.ui.case_manager.highlighter import MyHighlighter
from uitester.ui.case_manager.tag_manage_widget import TagManageWidget
from uitester.ui.case_run.add_device import AddDeviceWidget
from uitester.ui.case_run.console import Console


class EditorWidget(QWidget):
    device_and_data_signal = pyqtSignal(list, int, name="device_list_signal")
    import_list_signal = pyqtSignal(set, name="import_list_signal")

    def __init__(self, refresh_signal, tester, case_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_editor.ui')
        uic.loadUi(ui_file_path, self)

        self.dBCommandLineHelper = DBCommandLineHelper()
        self.tester = tester
        self.config = self.tester.get_config()
        self.debug_runner = self.tester.get_debug_runner()
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
        self.editor_text_edit = TextEdit(self.debug_runner.core)  # case content TextEdit
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
        self.editor_text_edit.parse_error_info_signal.connect(self.add_info_console, Qt.QueuedConnection)

        # run status listener
        self.status_listener = EditorRunStatusListener()
        self.status_listener.editor_listener_msg_signal.connect(self.result_handle, Qt.QueuedConnection)
        self.debug_runner.listener = self.status_listener

        self.data_line = None

        # button event
        self.save_btn.clicked.connect(self.save_case)
        self.run_btn.clicked.connect(self.run_btn_event)
        self.console_btn.clicked.connect(self.log_show_hide_event)
        self.add_data_btn.clicked.connect(self.add_case_data)
        self.add_tag_button.clicked.connect(self.choose_event)
        # case data
        self.case_manager = CaseManager()

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
        save_icon.addPixmap(QPixmap(self.config.images + '/save.png'), QIcon.Normal, QIcon.Off)  # save icon
        self.save_btn.setIcon(save_icon)

        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)  # run icon
        self.run_btn.setIcon(run_icon)

        console_icon = QIcon()
        console_icon.addPixmap(QPixmap(self.config.images + '/console.png'), QIcon.Normal, QIcon.Off)  # console icon
        self.console_btn.setIcon(console_icon)

        add_data_icon = QIcon()
        add_data_icon.addPixmap(QPixmap(self.config.images + '/add.png'), QIcon.Normal, QIcon.Off)  # console icon
        self.add_data_btn.setIcon(add_data_icon)

    def add_case_data(self):
        """
        show case data widget
        :return:
        """
        if hasattr(self,'case_data_widget'):
            self.case_data_widget.close()
        self.case_data_widget = CaseDataWidget(self.case_id)
        self.case_data_widget.show()

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

    def add_info_console(self, info):
        """
        append error massage to console
        :param info:
        :return:
        """
        self.console.append(info)

    def result_handle(self, msg, is_passed):
        """
        show the debug result in console
        :param is_passed:
        :param msg:
        :return:
        """
        if msg.status == 500:  # fail
            self.add_info_console("<font color='red'>" + str(msg.message) + "</font>")
        if msg.status == 102 and is_passed:
            self.add_info_console("<font color='green'> The case is Passed.</font>")
        elif msg.status == 102 and not is_passed:
            self.add_info_console("<font color='red'> The case is Failed.</font>")

    def set_case_edit_data(self):
        """
        init data for update case
        :return:
        """
        if not self.case_id:
            return
        self.case = self.dBCommandLineHelper.query_case_by_id(self.case_id)
        self.id_line_edit.setText(self.case_id)
        self.case_name_line_edit.setText(self.case.name)
        tags = ''
        for tag in self.case.tags:
            tags = tags + tag.name + ";"
        self.tag_names_line_edit.setText(tags)
        self.editor_text_edit.setPlainText(self.case.content)

        # 'import' block in the case content
        init_import_set = set()
        for cmd in self.case.content.split("\n"):
            if cmd.strip().find("import") == 0:
                init_import_set.add(cmd.strip())
        # send the init import block to editor's text edit, for init the highlighter and completer
        self.import_list_signal.emit(init_import_set)

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
        reply = self.message_box.question(self, "Save Changes?", "The case has been modified, save changes?",
                                          QMessageBox.Save | QMessageBox.Cancel | QMessageBox.Discard)

        if reply == QMessageBox.Save:  # update case info
            self.save_case(event)
        elif reply == QMessageBox.Discard:
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
        is_tags_names_modify = list(set(db_tag_list).difference(set(tag_list))) != list(
            set(tag_list).difference(set(db_tag_list)))

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
        self.device_and_data_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.add_device_widget.run_editor_signal.connect(self.run_case, Qt.QueuedConnection)
        devices = []
        if self.check_null():
            return
        if self.is_running:
            self.stop_case()
            return
        try:
            devices = self.tester.devices()
        except Exception as e:
            self.add_info_console("<font color='red'>" + str(e) + "</font>")
        if not devices:  # There is no device connected
            self.message_box.warning(self, "Message", "Please connect the device to your computer.", QMessageBox.Ok)
            return

        # get case data count
        case_data_manage = CaseDataManager()
        case_data_count = 0
        if self.case_id is not None:
            case_data_count = case_data_manage.get_case_data_count(self.case_id)

        self.device_and_data_signal.emit(devices, case_data_count)
        self.add_device_widget.show()

    def run_case(self, devices, data_line_number):
        # change icon
        stop_icon = QIcon()
        stop_icon.addPixmap(QPixmap(self.config.images + '/stop.png'), QIcon.Normal, QIcon.Off)
        self.run_btn.setIcon(stop_icon)
        self.run_btn.setText("Stop")
        self.is_running = True
        if not devices:
            return
        self.tester.select_devices(devices)

        self.data_line = data_line_number
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
            self.add_info_console("<font color='red'>" + str(e) + "</font>")

    def run(self):
        """
        run case content
        :return:
        """
        case_content = self.editor_text_edit.toPlainText().strip()
        try:
            self.debug_runner.reset()
            self.debug_runner.parse(case_content)
            self.debug_runner.execute(case_content, self.data_line)
        except Exception as e:
            self.stop_case()
            self.add_info_console("<font color='red'>" + str(e) + "</font>")
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

        if self.check_tag_name():  # check unrecognized tag names
            return

        if self.case_id:
            self.case.name = case_name
            self.case.content = content
            self.case.tags = tags
            if hasattr(self, 'case_data_widget') and self.case_data_widget.isVisible():
                self.case_manager.update_case(self.case_id, self.case_data_widget.case_data_list,
                                              self.case_data_widget.delete_data_ids)
                del self.case_data_widget.delete_data_ids[:]
            else:
                self.dBCommandLineHelper.update_case()
            self.message_box.information(self, "Update case", "Update case success.", QMessageBox.Ok)
        else:
            if hasattr(self, 'case_data_widget') and self.case_data_widget.isVisible():
                case = self.case_manager.insert_case(case_name, content, tags, self.case_data_widget.case_data_list,
                                                     self.case_data_widget.delete_data_ids)
                del self.case_data_widget.delete_data_ids[:]
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
            self.parse_import_as()
        func_dict = self.debug_runner.core.kw_func  # get default functions
        cmp = Completer(self.debug_runner)
        self.editor_text_edit.set_completer(cmp)

        # highlighter
        kw_list = []
        for func_name, func in func_dict.items():
            kw_list.append(func_name)
        self.high_lighter = MyHighlighter(self.editor_text_edit, kw_list)
        self.editor_text_edit.set_highlighter(self.high_lighter)

    def parse_import_as(self):
        """
        parse all the 'import' and 'as' block in the case content
        :return:
        """
        import_list = set()  # import list
        as_list = set()  # as list
        content_list = self.dBCommandLineHelper.query_case_by_id(self.case_id).content.split("\n")
        if not content_list:
            return
        for line in content_list:
            if line.strip().find("import") == 0:
                import_list.add(line.strip())
            elif " as " in line.strip():
                as_list.add(line.strip())
        self.debug_runner.core.kw_func.clear()
        self.debug_runner.core.kw_func = {**self.debug_runner.core.default_func}
        for import_line in import_list:
            try:
                self.debug_runner.core.parse_line(import_line)
            except Exception as e:
                self.add_info_console("<font color='red'>" + str(e) + "</font>")
        for as_line in as_list:
            try:
                self.debug_runner.core.parse_line(as_line)
            except Exception as e:
                self.add_info_console("<font color='red'>" + str(e) + "</font>")

    def set_tag_name_completer(self):
        """
        set completer to tag_names_line_edit
        :return:
        """
        # change button icon
        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(self.config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.add_tag_button.setIcon(add_icon)
        self.add_tag_button.setToolTip("add tag")

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
