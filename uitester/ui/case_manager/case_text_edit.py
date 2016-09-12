# -*- encoding: UTF-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from uitester.ui.case_manager.completer_widget import CompleterWidget


class TextEdit(QTextEdit):
    insert_func_name_signal = pyqtSignal(str)
    parse_error_info_signal = pyqtSignal(str)

    def __init__(self, kw_core, parent=None):
        super(TextEdit, self).__init__(parent)
        self.cmp = None
        self.kw_core = kw_core
        self.popup_widget = CompleterWidget()
        self.insert_func_name_signal.connect(self.insert_completion, Qt.QueuedConnection)
        self.popup_widget.func_list_widget.select_signal.connect(self.insert_completion, Qt.QueuedConnection)
        self.popup_widget.selected_func_name_signal.connect(self.popup_widget.update_desc, Qt.QueuedConnection)
        self.textChanged.connect(self.text_change)
        self.high_lighter = None
        self.import_lines = set()

    def text_change(self):
        """
        text改变处理事件
        解决使用中文输入法输入时，keyPressEvent被输入法拦截，自动提示框无法及时弹出的问题
        :return:
        """
        completion_prefix = self.text_under_cursor()
        if len(completion_prefix) < 2:
            self.popup_widget.hide()
            return
        self.cmp.update(completion_prefix, self.popup_widget)
        self.update_popup_widget_position()
        self.activateWindow()

    def set_completer(self, completer):
        self.cmp = completer
        if not self.cmp:
            return
        self.cmp.setWidget(self)
        self.cmp.setCompletionMode(QCompleter.PopupCompletion)
        self.cmp.setCaseSensitivity(Qt.CaseInsensitive)

    def completer(self):
        return self.cmp

    def set_highlighter(self, high_lighter):
        self.high_lighter = high_lighter

    def insert_completion(self, string):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        tc.insertText(string)
        self.popup_widget.hide()   # insert the text into text edit, and hide the popup_widget
        self.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def mousePressEvent(self, event):
        """
        while the mouse pressed and the popup_widget is visible, hide the popup_widget
        :param event:
        :return:
        """
        if self.cmp and self.popup_widget.func_list_widget.isVisible():
            self.popup_widget.hide()
        super(TextEdit, self).mousePressEvent(event)

    def keyPressEvent(self, e):
        if self.cmp and self.popup_widget.func_list_widget.isVisible():
            current_row = self.popup_widget.func_list_widget.currentRow()
            # 上下键控制list
            if e.key() == Qt.Key_Down:
                self.current_item_down(current_row)
                return

            if e.key() == Qt.Key_Up:
                self.current_item_up(current_row)
                return

            if e.key() in (Qt.Key_Return, Qt.Key_Enter):
                self.insert_func_name_signal.emit(self.popup_widget.func_list_widget.currentItem().text())
                return

        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            # 逐行解析,update自动提示list
            self.parse_content()

        is_shortcut = ((e.modifiers() & Qt.ControlModifier) and e.key() == Qt.Key_E)  # 设置 ctrl + e 快捷键
        if not self.cmp or not is_shortcut:
            super(TextEdit, self).keyPressEvent(e)

        ctrl_or_shift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)
        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        has_modifier = (e.modifiers() != Qt.NoModifier) and not ctrl_or_shift
        completion_prefix = self.text_under_cursor()

        if not is_shortcut and (has_modifier or (not e.text()) or len(completion_prefix) < 2 or (e.text()[-1] in eow)):
            self.popup_widget.hide()
            return
        self.cmp.update(completion_prefix, self.popup_widget)
        self.update_popup_widget_position()
        self.activateWindow()

    def parse_content(self):
        """
        解析case内容,显示parse error信息到console
        :return:
        """
        self.parse_import()

        content_list = self.toPlainText().split("\n")
        row_index = self.textCursor().blockNumber()  # 光标所在行号
        line_content = content_list[row_index].strip()
        if not line_content:
            return
        if line_content.find('import') != 0:
            try:
                self.kw_core.parse_line(line_content)
            except ValueError as e:
                self.parse_error_info_signal.emit(str(e.args))

    def update_popup_widget_position(self):
        """
        更新提示框显示位置
        :return:
        """
        cursor_pos = self.cursorRect()  # 光标位置
        edit_pos = self.mapToGlobal(QPoint(10, 15))   # 获得TextEdit在屏幕中的坐标，QPoint(5, 10)中 5、10为距离光标的x、y偏移量
        x = edit_pos.x() + cursor_pos.x()
        y = edit_pos.y() + cursor_pos.y()
        self.popup_widget.setGeometry(x, y, 650, 280)    # 更新显示位置

    def get_import_from_content(self, init_import_lines=None):
        """
        获取content中的import语句
        :return:
        """
        current_import_lines = set()
        if init_import_lines:
            self.import_lines = init_import_lines
            return self.import_lines
        if not self.toPlainText():
            return current_import_lines
        content_list = self.toPlainText().split("\n")

        for line in content_list:
            if line.strip().find('import') == 0:
                current_import_lines.add(line.strip())
        return current_import_lines

    def parse_import(self):
        """
        解析case content中所有import语句
        :return:
        """
        current_import = self.get_import_from_content()

        # 判断import语句是否发生变化
        is_import_updated = (len(self.import_lines) == len(current_import)) and (list(current_import).sort() == list(self.import_lines).sort())
        if is_import_updated:
            return
        if self.kw_core.user_func != self.kw_core.default_func:
            self.kw_core.user_func.clear()
            self.kw_core.user_func = {**self.kw_core.default_func}
        self.import_lines = current_import
        for import_cmd in self.import_lines:
            self.kw_core.parse_line(import_cmd)
        self.update_completer_high_lighter()

    def update_completer_high_lighter(self):
        """
        更新自动提示以及高亮提示
        :return:
        """
        if not self.kw_core.user_func:
            return
        self.cmp.func_dict = self.kw_core.user_func  # 更新自动提示func_list
        # 更新高亮kw list
        kw_list = set()
        for func_name, func in self.cmp.func_dict.items():
            kw_list.add(func_name)
        self.high_lighter.__init__(self, kw_list)
        # 重新定位光标, 刷新高亮提示
        tc = self.textCursor()
        content = self.toPlainText()
        index = tc.position()
        # self.setText("")
        self.setText(content)
        tc.setPosition(index)
        self.setTextCursor(tc)
        self.activateWindow()

    def current_item_down(self, current_row):
        """
        向下移动选中项
        :param current_row:
        :return:
        """
        if current_row == self.popup_widget.func_list_widget.count() - 1:
            self.popup_widget.func_list_widget.setCurrentRow(current_row)
            return
        self.popup_widget.func_list_widget.setCurrentRow(current_row + 1)
        func_name = self.popup_widget.func_list_widget.currentItem().text()
        self.popup_widget.selected_func_name_signal.emit(func_name, self.cmp.func_dict)

    def current_item_up(self, current_row):
        """
        向上移动选中项
        :param current_row:
        :return:
        """
        if current_row == 0:
            self.popup_widget.func_list_widget.setCurrentRow(current_row)
            return
        self.popup_widget.func_list_widget.setCurrentRow(current_row - 1)
        func_name = self.popup_widget.func_list_widget.currentItem().text()
        self.popup_widget.selected_func_name_signal.emit(func_name, self.cmp.func_dict)


class Completer(QCompleter):
    def __init__(self, func_dict, parent=None):
        super(Completer, self).__init__(parent)
        self.func_dict = func_dict
        self.string_list = []

    def update(self, completion_text, popup_widget):
        self.string_list = self.get_func_name_list(self.func_dict)
        filtered = []
        popup_widget.func_list_widget.clear()
        for string in self.string_list:
            if (completion_text in string) and (completion_text != string):
                filtered.append(string)
                popup_widget.func_list_widget.addItem(string)
        popup_widget.func_list_widget.sortItems()  # 按升序排列

        if len(filtered) < 1:
            popup_widget.hide()
            return
        popup_widget.show()
        popup_widget.setFocusPolicy(Qt.NoFocus)
        popup_widget.func_list_widget.setCurrentRow(0)  # 设置默认选中项
        func_name = popup_widget.func_list_widget.currentItem().text()
        popup_widget.selected_func_name_signal.emit(func_name, self.func_dict)  # 发送signal，更新desc

    def get_func_name_list(self, func_dict):
        """
        获取func name列表
        :param func_dict:
        :return:
        """
        func_name_list = []
        for func_name, func in func_dict.items():
            func_name_list.append(func_name)
        return func_name_list
