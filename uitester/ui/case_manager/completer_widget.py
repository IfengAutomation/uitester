# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QListWidget, QTextBrowser

from uitester.ui.case_manager.func_list_widget import FuncNameListWidget


class CompleterWidget(QWidget):
    select_signal = pyqtSignal(str)
    selected_func_name_signal = pyqtSignal(str, dict)

    def __init__(self, parent=None):
        super(CompleterWidget, self).__init__(parent)

        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'completer_widget.ui')
        uic.loadUi(ui_file_path, self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # 去除标题栏、窗体置顶、隐藏任务栏图标 | Qt.WindowStaysOnTopHint

        self.func_list_widget = FuncNameListWidget()
        self.func_list_widget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.func_list_layout.insertWidget(0, self.func_list_widget)
        self.desc_text_browser.setSizeAdjustPolicy(QTextBrowser.AdjustToContents)

        self.func_list_widget.setFocusPolicy(Qt.NoFocus)

    def update_desc(self, text, func_dict):
        """
        根据选中的func name，更新帮助信息展示栏
        :param func_dict:
        :param text:
        :return:
        """
        if not text:
            return
        func_doc = func_dict[text].__doc__
        if not func_doc:  # 处理func对应帮助文档为空
            return
        func_doc = func_dict[text].__doc__.split("\n")
        func_desc = ''
        for line in func_doc:
            func_desc = func_desc + line.lstrip() + "\n"    # 逐行去除左侧空格
        self.desc_text_browser.setText("<pre> <font color='green'>" + func_desc + "</font></pre>")
