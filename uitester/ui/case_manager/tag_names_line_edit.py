from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtWidgets import QLineEdit, QCompleter


class TagNamesLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(QLineEdit, self).__init__(parent)
        self.cmp = None
        self.is_completer = True

    def setCompleter(self, completer):
        self.cmp = completer
        self.cmp.setWidget(self)
        self.cmp.setCompletionMode(QCompleter.PopupCompletion)
        self.cmp.setCaseSensitivity(Qt.CaseInsensitive)
        self.textChanged.connect(self.tag_names_changed)
        self.cmp.activated.connect(self.insert_completion)

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
        else:
            pass

    def completer(self):
        return self.cmp

    def insert_completion(self, string):
        text = self.text()
        tag_names = text.split(';')
        last_tag_name = tag_names[len(tag_names) - 1]
        new_text = text[0:len(text) - len(last_tag_name)] + string + ';'
        self.is_completer = False
        self.clear()
        self.setText(new_text)
        self.is_completer = True


class TagCompleter(QCompleter):
    def __init__(self, string_list, parent=None):
        super(TagCompleter, self).__init__(parent)
        self.string_list = string_list
        self.setModel(QStringListModel())

    def update(self, completion_text):
        filtered = []
        for string in self.string_list:
            if completion_text in string:
                filtered.append(string)
        self.model().setStringList(filtered)
        self.popup().setCurrentIndex(self.model().index(0, 0))

