from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTextBrowser, QAction


class Console(QTextBrowser):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.menu = None

    def contextMenuEvent(self, event):
        if self.menu:
            del self.menu
            self.menu = None
        self.menu = self.createStandardContextMenu()

        clear_action = QAction("Clear", self.menu)
        self.menu.addAction(clear_action)   # add clear action

        if not self.toPlainText():   # content is None
            clear_action.setDisabled(True)
        else:
            clear_action.setDisabled(False)
            clear_action.triggered.connect(self.clear_text)  # connect clear event
        self.menu.exec(QCursor().pos())

    def clear_text(self):
        """
        clear the textBrowser
        :return:
        """
        self.clear()
