# @Time    : 2016/8/17 10:56
# @Author  : lixintong
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget

from uitester.ui.case_manager.case_manager_ui import CaseManagerUi


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'mainwindow.ui')
        uic.loadUi(ui_file_path, self)
        # todo 更改窗体大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.setWindowTitle("test-manager")
        case_manager_widget = CaseManagerUi()
        self.tabWidget.addTab(case_manager_widget, "case_manager")


def start():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
