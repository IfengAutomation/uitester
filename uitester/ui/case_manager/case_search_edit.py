# @Time    : 2016/8/18 13:37
# @Author  : lixintong

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLineEdit, QCompleter, QPushButton, QHBoxLayout

from uitester.config import Config


class SearchLayout(QHBoxLayout):
    def __init__(self, tag_names_line_edit, search_button):
        super().__init__()
        self.tag_names_line_edit = tag_names_line_edit
        self.search_button = search_button
        margins = self.tag_names_line_edit.textMargins()
        self.tag_names_line_edit.setTextMargins(margins.left(), margins.top(), self.search_button.width(),
                                                margins.bottom())
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.addWidget(self.search_button)
        self.tag_names_line_edit.setLayout(self)


class SearchButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setToolTip("search case")
        search_icon = QIcon()
        config = Config()
        search_icon.addPixmap(QPixmap(config.images + '/search.png'), QIcon.Normal, QIcon.Off)
        self.setIcon(search_icon)
        # self.setText("Search")
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(22, 22)
        self.setStyleSheet(
            # "QPushButton{border-width:0px; background:transparent;} "
            "border:none; "
        )


class TagLineEdit(QLineEdit):
    def __init__(self, name, search_button, parent=None):
        super(QLineEdit, self).__init__(parent)
        self.setObjectName(name)
        self.cmp = None
        self.is_completer = True
        self.setPlaceholderText("tag names")
        self.tag_edit_layout = QHBoxLayout()
        self.tag_edit_layout.setSpacing(0)
        self.tag_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.tag_edit_layout.addStretch()
        self.tag_edit_layout.addWidget(search_button)
        margins = self.textMargins()
        self.setTextMargins(margins.left(), margins.top(), search_button.width(),
                            margins.bottom())
        self.setLayout(self.tag_edit_layout)

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
    def __init__(self, string_list, parent=None):
        super(TagCompleter, self).__init__(parent)
        self.string_list = string_list
        self.setModel(QStringListModel())

    def update(self, completion_text):
        filtered = []
        for str in self.string_list:
            if completion_text in str:
                filtered.append(str)
        self.model().setStringList(filtered)
        self.popup().setCurrentIndex(self.model().index(0, 0))
