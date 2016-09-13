# @Time    : 2016/8/17 10:56
# @Author  : lixintong
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget

from uitester.tester import Tester
from uitester.ui.case_manager.case_manager import CaseManagerWidget
from uitester.ui.case_run.case_run import RunWidget


class MainWindow(QMainWindow):
    tester = Tester()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'mainwindow.ui')
        uic.loadUi(ui_file_path, self)
        # todo 更改窗体大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 2, screen.height() / 2)
        self.setMinimumSize(700, 350)
        self.setWindowTitle("uitest")
        self.move((screen.width() - self.width()) / 2, (screen.height() - self.height()) / 2)#draw centered
        # Add tab "Case"
        case_manager_widget = CaseManagerWidget(self.tester)
        self.tabWidget.addTab(case_manager_widget, "Case")

        # Add tab "Run"
        case_run_widget = RunWidget(self.tester)
        self.tabWidget.addTab(case_run_widget, "Run")

def start():
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
