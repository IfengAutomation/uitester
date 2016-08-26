import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)
        self.cmp = None

    def set_completer(self, completer):
        if self.cmp:
            self.disconnect(self.cmp, 0, 0)
        self.cmp = completer
        if not self.cmp:
            return
        self.cmp.setWidget(self)
        self.cmp.setCompletionMode(QCompleter.PopupCompletion)
        self.cmp.setCaseSensitivity(Qt.CaseInsensitive)
        self.cmp.activated.connect(self.insert_completion)

    def completer(self):
        return self.cmp

    def insert_completion(self, string):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        tc.insertText(string)
        self.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def keyPressEvent(self, e):
        if self.cmp and self.cmp.popup().isVisible():
            if e.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                e.ignore()
                return
        is_shortcut = ((e.modifiers() & Qt.ControlModifier) and e.key() == Qt.Key_E)
        if not self.cmp or not is_shortcut:
            super(TextEdit, self).keyPressEvent(e)

        ctrl_or_shift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="
        has_modifier = (e.modifiers() != Qt.NoModifier) and not ctrl_or_shift
        completion_prefix = self.text_under_cursor()

        if not is_shortcut and (has_modifier or (not e.text()) or len(completion_prefix) < 2 or (e.text()[-1] in eow)):
            self.cmp.popup().hide()
            return
        self.cmp.update(completion_prefix)
        self.cmp.popup().setCurrentIndex(self.cmp.completionModel().index(0, 0))
        cr = self.cursorRect()
        cr.setWidth(self.cmp.popup().sizeHintForColumn(0) + self.cmp.popup().verticalScrollBar().sizeHint().width())
        self.cmp.complete(cr)


class Completer(QCompleter):
    def __init__(self, string_list, parent=None):
        super(Completer, self).__init__(parent)
        self.string_list = string_list
        self.setModel(QStringListModel())

    def update(self, completion_text):
        filtered = []
        for string in self.string_list:
            if completion_text in string:
                filtered.append(string)
        self.model().setStringList(filtered)
        self.popup().setCurrentIndex(self.model().index(0, 0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    li = ['The', 'that', 'this', 'Red', 'right', 'what']
    cmp = Completer(li)
    window = QMainWindow()
    edit = TextEdit()
    edit.set_completer(cmp)
    window.setCentralWidget(edit)
    window.show()
    app.exec_()
