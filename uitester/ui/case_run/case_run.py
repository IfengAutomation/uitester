# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QMessageBox, QListWidget

from uitester.case_manager.database import DBCommandLineHelper
from uitester.ui.case_run.add_case import AddCaseWidget
from uitester.ui.case_run.add_device import AddDeviceWidget
from uitester.ui.case_run.table_widget import RunnerTableWidget


class RunWidget(QWidget):
    running = False
    device_list_signal = pyqtSignal(list, list)
    cases = []

    def __init__(self, tester, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_run.ui')
        uic.loadUi(ui_file_path, self)

        # set icon
        run_icon = QIcon()
        self.tester = tester
        self.config = self.tester.get_config()

        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(run_icon)

        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(self.config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.addbtn.setIcon(add_icon)

        self.message_box = QMessageBox()

        self.dBCommandLineHelper = DBCommandLineHelper()

        self.addbtn.clicked.connect(self.click_add_case)
        self.run_stop_btn.clicked.connect(self.click_run_stop_btn)

        self.add_case_widget = AddCaseWidget()
        self.add_device_widget = AddDeviceWidget()
        self.add_device_widget.setWindowModality(Qt.ApplicationModal)

        self.case_widget = QListWidget()
        self.case_table_layout.insertWidget(0, self.case_widget)

        # add log 连接
        self.add_device_widget.add_log_signal.connect(self.add_log, Qt.QueuedConnection)
        self.add_device_widget.run_signal.connect(self.run_case, Qt.QueuedConnection)
        self.device_list_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.add_case_widget.select_case_signal.connect(self.show_cases, Qt.QueuedConnection)

    def click_add_case(self):
        self.add_case_widget.setWindowModality(Qt.ApplicationModal)  # 设置QWidget为模态
        self.add_case_widget.show()

    def click_run_stop_btn(self):
        if self.running:
            self.stop_case()
            return
        if not self.cases:  # cases is null
            # 提示 case未选
            self.message_box.warning(self, "Message", "Please add cases first.", QMessageBox.Ok)
            return
        if not self.tester.devices():
            self.message_box.warning(self, "Message", "Please connect your device first.", QMessageBox.Ok)
            return
        self.add_device_widget.show()
        self.device_list_signal.emit(self.tester.devices(), self.cases)

    def add_log(self, log_info):
        """
        add log to logarea
        :return:
        """
        if self.logarea is None:
            return
        self.logarea.append(log_info)

    def update_case_name_color(self, case_id, result):
        """
        根据执行结果对case name着色 pass: green; fail: red
        :param case_id:
        :param result:
        :return:
        """
        model = self.case_table_view.model()
        for column_index in range(model.rowCount()):
            index = model.index(column_index, 0)
            cell_content = model.data(index)
            if str(case_id) == str(cell_content):
                if result == 1:  # case pass
                    model.item(column_index, 1).setForeground(QBrush(QColor(55, 177, 88)))  # 设置字体颜色 绿色
                    self.case_table_view.selectRow(column_index)
                else:   # case fail
                    model.item(column_index, 1).setForeground(QBrush(QColor(255, 0, 0)))  # 设置字体颜色 红色
                return

    def run_case(self):
        # 图标变为stop
        # set icon
        stop_icon = QIcon()
        stop_icon.addPixmap(QPixmap(self.config.images + '/stop.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(stop_icon)
        self.run_stop_btn.setText("Stop")
        self.running = True
        # TODO 调用tester中提供方法run case

    def stop_case(self):
        # set icon
        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(run_icon)
        self.run_stop_btn.setText("Run")
        self.running = False
        # TODO 停止执行

    def show_cases(self, id_list):
        """
        根据id去数据库中拿到Case对象，展示Case对象的casename
        :param id_list:
        :return:
        """
        self.case_widget.setParent(None)
        self.case_table_layout.removeWidget(self.case_widget)
        case_list = []
        self.cases = id_list
        for case_id in id_list:
            case = self.dBCommandLineHelper.query_case_by_id(case_id)
            case_list.append(case)
        self.case_widget = RunnerTableWidget(case_list, [0])
        self.case_table_layout.insertWidget(0, self.case_widget)

