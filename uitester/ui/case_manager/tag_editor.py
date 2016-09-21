# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config


class TagEditorWidget(QWidget):
    def __init__(self, refresh_signal, tag_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refresh_signal = refresh_signal
        self.db_helper = DBCommandLineHelper()
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'tag_editor.ui')
        uic.loadUi(ui_file_path, self)
        # set icon
        save_icon = QIcon()
        config = Config()
        save_icon.addPixmap(QPixmap(config.images + '/save.png'), QIcon.Normal, QIcon.Off)
        self.tag_save_btn.setIcon(save_icon)
        self.tag_save_btn.clicked.connect(self.tag_save)
        self.tag_id_line_edit.hide()  # 隐藏line_edit
        self.tag_name_line_edit.setPlaceholderText("Tag Name")  # 设置提示文字
        self.tag_description_text_edit.setPlaceholderText('tag description')
        if tag_name:
            self.tag = self.db_helper.query_tag_by_name(tag_name)
            self.tag_id_line_edit.setText(str(self.tag.id))
            self.tag_name_line_edit.setText(self.tag.name)
            self.tag_description_text_edit.setPlainText(self.tag.description)
            # self.tag_description_text_edit.setDocument(QTextDocument("Tag description"))  # 设置提示文字

    def closeEvent(self, close_even):
        if self.tag_id_line_edit.text() != '':
            if self.tag.name != self.tag_name_line_edit.text() or self.tag.description != self.tag_description_text_edit.toPlainText():
                reply = QMessageBox.information(self, 'close window', 'Changes not saved, confirm close?',
                                                QMessageBox.Yes, QMessageBox.No)
                if reply != QMessageBox.Yes:
                    close_even.ignore()
                    return
        else:
            if self.tag_id_line_edit.text() != '' or self.tag_description_text_edit.toPlainText() != '':
                reply = QMessageBox.information(self, 'close window', 'Changes not saved, confirm close?',
                                                QMessageBox.Yes, QMessageBox.No)
                if reply != QMessageBox.Yes:
                    close_even.ignore()
                    return
        self.refresh_signal.emit()

    def tag_save(self):
        tag_id = self.tag_id_line_edit.text()
        tag_name = self.tag_name_line_edit.text()
        tag_description = self.tag_description_text_edit.toPlainText()
        if tag_name == '' or tag_description == '':
            QMessageBox.warning(self, 'tag editor', 'tag name and description can\'t be empty')
        else:
            if len(tag_name) > 8:
                QMessageBox.warning(self, 'tag editor', 'tag name is not greater than 8 characters')
            else:
                if tag_id:
                    self.tag.name = tag_name
                    self.tag.description = tag_description
                    self.db_helper.update_tag()
                    QMessageBox.information(self, 'tag editor', 'tag update success')#todo 是否添加刷新
                else:
                    tag = self.db_helper.query_tag_by_name(tag_name)
                    if tag is None:
                        tag = self.db_helper.insert_tag(tag_name, tag_description)
                        self.tag_id_line_edit.setText(str(tag.id))
                        self.tag = tag
                        QMessageBox.information(self, 'tag editor', 'tag insert success')#todo 是否添加刷新
                    else:
                        QMessageBox.warning(self, 'tag editor', 'tag has existed')
