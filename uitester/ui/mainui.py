from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'main.ui')
        uic.loadUi(ui_file_path, self)
        self.addBtn.clicked.connect(self.add_item)
        self.rmBtn.clicked.connect(self.rm_item)
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

    def add_item(self):
        self.model.appendRow(QStandardItem('Hello , world!!'))

    def rm_item(self):
        self.model.removeRow(self.model.rowCount()-1)


def start():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
