# @Time    : 2016/8/30 15:46
# @Author  : lixintong
import math
import os
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QImage, QPixmap, QMovie
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QLabel

from uitester.config import Config


class ConflictTagsWidget(QWidget):
    def __init__(self, conflict_tags_message_dict, case_data_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_data_manager = case_data_manager
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, "conflict_tag.ui")
        uic.loadUi(ui_file_path, self)
        self.setWindowTitle("conflict tag")
        self.conflict_tags_message_dict = conflict_tags_message_dict
        self.set_conflict_tags_table_widget()

        config = Config()
        image = QImage(os.path.join(config.images, 'notice.png'))
        result = image.scaled(40, 40)
        self.notice_image_label.setPixmap(QPixmap.fromImage(result))
        self.notice_image_label.setAlignment(Qt.AlignCenter)
        self.notice_text_label.setText(
            '合并标识冲突说明：\n'
            '1、确认标识名称与现有标识名称是否含义一致，不一致可修改标识名称\n'
            '2、信息确认后，点击提交进行合并')
        self.conflict_tags_submit_button.clicked.connect(self.conflict_tags_submit)
        self.button_style(self.conflict_tags_submit_button)
        self.cancel_submit_button.clicked.connect(self.cancel_submit)
        self.button_style(self.cancel_submit_button)

    def button_style(self, button):
        button.setStyleSheet("QPushButton{ background:#ECF5FF;} "
                             "QPushButton:hover{background:#C4E1FF ;}"
                             "QPushButton:pressed{background:#ACD6FF ;}"
                             )

    def cancel_submit(self):
        self.close()

    def set_conflict_tags_table_widget(self):
        self.conflict_tag_table_widget.setColumnCount(5)
        self.conflict_tag_table_widget.setRowCount(len(self.conflict_tags_message_dict.keys()))
        # set table header
        self.conflict_tag_table_widget.setHorizontalHeaderItem(0, QTableWidgetItem('标识Id'))
        self.conflict_tag_table_widget.setHorizontalHeaderItem(1, QTableWidgetItem('标识名称'))
        self.conflict_tag_table_widget.setHorizontalHeaderItem(2, QTableWidgetItem('标识描述'))
        self.conflict_tag_table_widget.setHorizontalHeaderItem(3, QTableWidgetItem('现有标识名称'))
        self.conflict_tag_table_widget.setHorizontalHeaderItem(4, QTableWidgetItem('现有标识描述'))
        self.conflict_tag_table_widget.horizontalHeader().setStyleSheet("QHeaderView::section{background:	#ECF5FF;}")
        self.conflict_tag_table_widget.horizontalHeader().setStretchLastSection(True)
        # set table data
        row = 0
        for key in self.conflict_tags_message_dict:
            conflict_tag = self.conflict_tags_message_dict[key]
            self.conflict_tag_table_widget.setItem(row, 0, QTableWidgetItem(str(conflict_tag['id'])))
            # tag_name
            tag_name_item = QTableWidgetItem(conflict_tag['name'])
            tag_name_item.setForeground(Qt.red)
            tag_name_item.setFont(QFont("Times", 10, QFont.Black))
            self.conflict_tag_table_widget.setItem(row, 1, tag_name_item)

            # tag_description
            if type(conflict_tag['description']) is float and math.isnan(conflict_tag['description']):
                description = ''
            else:
                description = conflict_tag['description']
            self.conflict_tag_table_widget.setItem(row, 2, QTableWidgetItem(description))

            src_name_widget_item = QTableWidgetItem(conflict_tag['src_name'])
            src_name_widget_item.setFlags(Qt.NoItemFlags)
            self.conflict_tag_table_widget.setItem(row, 3, src_name_widget_item)
            if type(conflict_tag['src_description']) is float and math.isnan(conflict_tag['src_description']):
                src_description = ''
            else:
                src_description = conflict_tag['src_description']
            src_description_widget_item = QTableWidgetItem(src_description)
            src_description_widget_item.setFlags(Qt.NoItemFlags)
            self.conflict_tag_table_widget.setItem(row, 4, src_description_widget_item)
            row += 1
        self.conflict_tag_table_widget.setColumnHidden(0, True)
        self.conflict_tag_table_widget.setColumnHidden(3, True)
        self.conflict_tag_table_widget.setColumnHidden(4, True)

    def callback(self,result):
        if result:
            self.wait_dialog.close()
            self.close()

    def conflict_tags_submit(self):
        """
        submit conflict tags
        :return:
        """
        updata_tag_message_list = self.get_table_data()
        again_conflict_data = self.get_conflict_data(updata_tag_message_list)
        self.wait_dialog = WaitDialog(self)
        self.wait_dialog.setWindowModality(Qt.ApplicationModal)
        if again_conflict_data:
            message = str(again_conflict_data) + " 已存在，是否继续提交"
            reply = QMessageBox.information(self, "合并冲突", message, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                thread = Thread(target=self.case_data_manager.merge_conflict_data_callback, args=(updata_tag_message_list, self.callback))
                thread.start()
        else:
            self.wait_dialog.show()
            thread = Thread(target=self.case_data_manager.merge_conflict_data_callback, args=(updata_tag_message_list, self.callback))
            thread.start()

    def get_table_data(self):
        table_data = []
        for row in range(0, self.conflict_tag_table_widget.rowCount()):
            table_item_data = {'id': int(self.conflict_tag_table_widget.item(row, 0).text()),
                               'name': self.conflict_tag_table_widget.item(row, 1).text(),
                               'description': self.conflict_tag_table_widget.item(row, 2).text(),
                               'src_name': self.conflict_tag_table_widget.item(row, 3).text(),
                               'src_description': self.conflict_tag_table_widget.item(row, 4).text()}
            table_data.append(table_item_data)
        return table_data

    def get_conflict_data(self, table_data):
        again_conflict_data = []
        for item_data in table_data:
            if item_data['name'] != item_data['src_name']:
                tag = self.case_data_manager.db_command_line_helper.query_tag_by_name(True, item_data['name'])
                if tag:
                    again_conflict_data.append(item_data['name'])
        return again_conflict_data


class WaitDialog(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super(WaitDialog, self).__init__(parent)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setFixedSize(181, 181)
        self.setWindowOpacity(0.5)  # set transparent
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)  # background transparent
        self.setContentsMargins(0, 0, 0, 0)
        config = Config()
        self.movie = QMovie(os.path.join(config.images, 'wait.gif'))
        self.label.setMovie(self.movie)
        self.movie.start()
