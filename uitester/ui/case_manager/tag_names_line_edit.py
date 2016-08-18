# @Time    : 2016/8/18 13:37
# @Author  : lixintong
import sys
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QLineEdit, QCompleter, QApplication, QMainWindow


class TagLineEdit(QLineEdit):
    def __init__(self, name, parent=None):
        super(QLineEdit, self).__init__(parent)
        self.setObjectName(name)
        self.cmp = None
        self.is_completer = True

    def setCompleter(self, completer):
        self.cmp = completer
        self.cmp.setWidget(self)
        self.cmp.setCompletionMode(QCompleter.PopupCompletion)
        self.cmp.setCaseSensitivity(Qt.CaseInsensitive)
        self.textChanged.connect(self.tag_names_changed)
        self.cmp.activated.connect(self.insertCompletion)

    def tag_names_changed(self):
        if self.is_completer:
            text = self.text()
            tag_names = text.split(';')
            last_tag_name = tag_names[len(tag_names) - 1]
            self.cmp.update(last_tag_name)
            self.cmp.popup().setCurrentIndex(self.cmp.completionModel().index(0, 0))
            cr = self.cursorRect()
            cr.setWidth(self.cmp.popup().sizeHintForColumn(0)
                        + self.cmp.popup().verticalScrollBar().sizeHint().width())
            self.cmp.complete(cr)
            pass
        else:
            pass

    def completer(self):
        return self.cmp

    def insertCompletion(self, string):
        text = self.text()
        tag_names = text.split(';')
        last_tag_name = tag_names[len(tag_names) - 1]
        new_text = text[0:len(text) - len(last_tag_name)] + string + ';'
        self.is_completer = False
        self.clear()
        self.setText(new_text)
        self.is_completer = True

    def textUnderCursor(self):
        text = self.text()
        tag_names = text.split(';')
        return tag_names[len(tag_names) - 1]


class TagCompleter(QCompleter):
    def __init__(self, stringlist, parent=None):
        super(TagCompleter, self).__init__(parent)
        self.stringlist = stringlist
        self.setModel(QStringListModel())

    def update(self, completionText):
        filtered = []
        for str in self.stringlist:
            if completionText in str:
                filtered.append(str)
        self.model().setStringList(filtered)
        self.popup().setCurrentIndex(self.model().index(0, 0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    li = ['直播', '点播', '专题', '军事']
    cmp = TagCompleter(li)
    window = QMainWindow()
    edit = TagLineEdit()
    edit.setCompleter(cmp)
    window.setCentralWidget(edit)
    window.show()
    app.exec_()
