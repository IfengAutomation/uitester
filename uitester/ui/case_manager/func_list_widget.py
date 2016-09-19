from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QListWidget


class FuncNameListWidget(QListWidget):
    select_signal = pyqtSignal(str, name="select_signal")

    def __init__(self, parent=None):
        super(FuncNameListWidget, self).__init__(parent)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Down:
            self.setCurrentRow(self.currentRow() + 1)
        elif e.key() == Qt.Key_Up:
            self.setCurrentRow(self.currentRow() - 1)
        elif e.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.select_signal.emit(self.currentItem().text())
