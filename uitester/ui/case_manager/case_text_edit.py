# -*- encoding: UTF-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from uitester.ui.case_manager.completer_widget import CompleterWidget


class TextEdit(QTextEdit):
    insert_func_name_signal = pyqtSignal(str, name="insert_func_name_signal")
    parse_error_info_signal = pyqtSignal(str, name="parse_error_info_signal")

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
        editor content change event
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
        parse the editor's content,and show the error massage in console
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
        set completer widget's position
        :return:
        """
        cursor_pos = self.cursorRect()
        edit_pos = self.mapToGlobal(QPoint(10, 15))
        x = edit_pos.x() + cursor_pos.x()
        y = edit_pos.y() + cursor_pos.y()
        self.popup_widget.setGeometry(x, y, 650, 280)

    def get_import_from_content(self, init_import_lines=None):
        """
        get all 'import' block from edit text
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
        parse the 'import' block
        :return:
        """
        current_import = self.get_import_from_content()

        # check the changes between the case content in db and the edit text content
        is_import_updated = (len(self.import_lines) == len(current_import)) and (list(current_import).sort() == list(self.import_lines).sort())
        if is_import_updated:
            return
        if self.kw_core.user_func != self.kw_core.default_func:
            self.kw_core.user_func.clear()
            self.kw_core.user_func = {**self.kw_core.default_func}
        self.import_lines = current_import
        for import_cmd in self.import_lines:
            try:
                self.kw_core.parse_line(import_cmd)
            except Exception as e:
                self.parse_error_info_signal.emit(str(e))
        self.update_completer_high_lighter()

    def update_completer_high_lighter(self):
        """
        update completer and high lighter
        :return:
        """
        if not self.kw_core.user_func:
            return
        self.cmp.func_dict = self.kw_core.user_func  # update completer's func_list
        # update highlighter's kw list
        kw_list = set()
        for func_name, func in self.cmp.func_dict.items():
            kw_list.add(func_name)
        self.high_lighter.__init__(self, kw_list)
        # refresh the text
        tc = self.textCursor()
        content = self.toPlainText()
        index = tc.position()
        self.setText(content)
        tc.setPosition(index)
        self.setTextCursor(tc)
        self.activateWindow()

    def current_item_down(self, current_row):
        """
        move down to the next item
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
        move up to the previous item
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
        popup_widget.func_list_widget.sortItems()  # ASC

        if len(filtered) < 1:
            popup_widget.hide()
            return
        popup_widget.show()
        popup_widget.setFocusPolicy(Qt.NoFocus)
        popup_widget.func_list_widget.setCurrentRow(0)
        func_name = popup_widget.func_list_widget.currentItem().text()
        popup_widget.selected_func_name_signal.emit(func_name, self.func_dict)

    def get_func_name_list(self, func_dict):
        """
        get function name list
        :param func_dict:
        :return:
        """
        func_name_list = []
        for func_name, func in func_dict.items():
            func_name_list.append(func_name)
        return func_name_list
