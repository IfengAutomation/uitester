import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.tag_editor import TagEditorWidget
from uitester.ui.case_manager.tag_names_line_edit import TagNamesLineEdit, TagCompleter


class TagManageWidget(QWidget):
    selected_tag_names_signal = pyqtSignal(str, name="selected_tag_names_signal")
    refresh_signal = pyqtSignal(name="refresh_signal")

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'tag_manage_widget.ui')
        uic.loadUi(ui_file_path, self)

        self.db_helper = DBCommandLineHelper()
        self.message_box = QMessageBox()

        self.tag_names_line_edit = TagNamesLineEdit()
        self.tag_names_line_edit.setPlaceholderText("Tag Names")
        self.cmp = None
        self.set_completer()
        self.selected_tag_names_layout.insertWidget(0, self.tag_names_line_edit)

        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.new_tag_btn.setIcon(add_icon)
        self.tag_editor = None
        self.tag_list = None
        self.set_tag_list_widget()   # init data

        self.select_btn.clicked.connect(self.select_event)
        self.cancel_btn.clicked.connect(self.close)
        self.new_tag_btn.clicked.connect(self.new_tag_event)

        self.refresh_signal.connect(self.set_tag_list_widget, Qt.QueuedConnection)

    def new_tag_event(self):
        """
        show tag editor
        :return:
        """
        self.tag_editor = TagEditorWidget(self.refresh_signal)
        self.tag_editor.setWindowModality(Qt.ApplicationModal)
        self.tag_editor.show()

    def select_event(self):
        """
        handle select event
        :return:
        """
        selected_tag_names = self.tag_names_line_edit.text().strip()
        if not selected_tag_names:
            self.close()
            return
        if self.check_tag_name():
            return
        self.selected_tag_names_signal.emit(selected_tag_names)
        self.close()

    def set_tag_list_widget(self):
        """
        init tag_list_widget data and onclick event
        :return:
        """
        self.tag_list_widget.clear()
        self.tag_list = self.db_helper.query_tag_all()
        for tag in self.tag_list:
            self.tag_list_widget.addItem(tag.name)
        self.tag_list_widget.itemClicked.connect(
            lambda: self.list_widget_item_clicked(self.tag_list_widget.currentItem()))
        item = self.tag_list_widget.item(0)
        if not item:
            return
        item.setSelected(True)
        self.set_completer()   # reset completer's tag name list

    def list_widget_item_clicked(self, tag_list_widget_item):
        """
        handle list widget item click event
        :param tag_list_widget_item:
        :return:
        """
        tag_name_set = set()
        selected_tag_names = ""

        selected_line_edit_text = self.tag_names_line_edit.text().strip()
        tag_names_list = selected_line_edit_text.split(";")

        # origin tag names
        for tag_name in tag_names_list:
            if tag_name.strip():
                tag_name_set.add(tag_name.strip() + ";")
        tag_name_set.add(tag_list_widget_item.text() + ';')  # add clicked tag name

        for tag_name in tag_name_set:
            selected_tag_names += tag_name
        self.tag_names_line_edit.is_completer = False
        self.tag_names_line_edit.clear()
        self.tag_names_line_edit.setText(selected_tag_names)
        self.tag_names_line_edit.is_completer = True

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
            tag = self.db_helper.query_tag_by_name(tag_name.strip())
            if not tag:
                unrecognized_tag_names += "\"" + tag_name + "\"" + "、"
        if not unrecognized_tag_names:
            return has_unrecognized
        has_unrecognized = True
        unrecognized_tag_names = unrecognized_tag_names[:-1]
        self.message_box.about(self, "Warning", "Tag name: " + unrecognized_tag_names +
                               " unrecognized, please add it first.")
        return has_unrecognized

    def set_completer(self):
        """
        set completer to tag_names_line_edit
        :return:
        """
        self.tag_list = self.db_helper.query_tag_all()  # get all tag
        tag_name_list = []
        for tag in self.tag_list:
            tag_name_list.append(tag.name)
        cmp = TagCompleter(tag_name_list)
        self.tag_names_line_edit.setCompleter(cmp)
