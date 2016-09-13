import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_manager.tag_editor import TagEditorWidget


class TagManageWidget(QWidget):
    selected_tag_names_signal = pyqtSignal(str)
    refresh_signal = pyqtSignal()

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'tag_manage_widget.ui')
        uic.loadUi(ui_file_path, self)

        self.db_helper = DBCommandLineHelper()
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
        selected_tag_names = self.selected_line_edit.text()
        if not selected_tag_names:
            self.close()
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
        item.setSelected(True)

    def list_widget_item_clicked(self, tag_list_widget_item):
        """
        handle list widget item click event
        :param tag_list_widget_item:
        :return:
        """
        tag_name_set = set()
        selected_tag_names = ""

        selected_line_edit_text = self.selected_line_edit.text()
        tag_names_list = selected_line_edit_text.split(";")
        for tag_name in tag_names_list:
            if tag_name:
                tag_name_set.add(tag_name + ";")
        tag_name_set.add(tag_list_widget_item.text() + ';')

        for tag_name in tag_name_set:
            selected_tag_names += tag_name

        self.selected_line_edit.clear()
        self.selected_line_edit.setText(selected_tag_names)
