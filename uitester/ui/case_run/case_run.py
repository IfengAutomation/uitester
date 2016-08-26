# -*- encoding: UTF-8 -*-
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QTextCharFormat
from PyQt5.QtWidgets import QWidget

from uitester.case_manager.database import DBCommandLineHelper
from uitester.config import Config
from uitester.ui.case_run.add_case import AddCaseWidget
from uitester.ui.case_run.add_device import AddDeviceWidget

cases = []


class RunWidget(QWidget):
    running = False
    device_list_signal = pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'case_run.ui')
        uic.loadUi(ui_file_path, self)

        # set icon
        run_icon = QIcon()
        self.config = Config()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(run_icon)

        add_icon = QIcon()
        add_icon.addPixmap(QPixmap(self.config.images + '/add.png'), QIcon.Normal, QIcon.Off)
        self.addbtn.setIcon(add_icon)

        self.dBCommandLineHelper = DBCommandLineHelper()

        self.addbtn.clicked.connect(self.click_add_case)
        self.run_stop_btn.clicked.connect(self.click_run_stop_btn)

        self.add_case_widget = AddCaseWidget()
        self.add_device_widget = AddDeviceWidget()

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
        self.add_device_widget.setWindowModality(Qt.ApplicationModal)
        self.device_list_signal.disconnect(self.add_device_widget.add_radio_to_widget)
        self.device_list_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)
        self.add_device_widget.show()
        self.device_list_signal.emit(self.add_device_widget.list_devices())

    def list_devices(self):
        """
        通过adb命令获取当前连接的device
        :return:
        """
        # TODO 暂时用此方法调试，最终会用tester中提供的方法
        cmd_adb_devices = 'adb devices'
        r = os.popen(cmd_adb_devices)
        info = r.readlines()
        devices = []
        for line in info:
            line = line.strip('\r\n')
            if line != 'List of devices attached' and line:
                device_id = line.split("	")[0]
                devices.append(device_id)
        return devices

    def add_log(self, log_info):
        """
        add log to logarea
        :return:
        """
        if self.logarea is None:
            return
        self.logarea.append(log_info)

    def update_case_color(self, case_name):
        # TODO 根据执行结果对case name着色 pass: green; fail: red
        keyword = QTextCharFormat()
        brush = QBrush(Qt.darkGreen, Qt.SolidPattern)
        case_name.setForeground(brush)

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
        # TODO 根据id去数据库中拿到Case对象，展示Case对象的casename
        case_list = []
        for case_id in id_list:
            case = self.dBCommandLineHelper.query_case_by_id(case_id)
            case_list.append(case)
            self.casearea.append(case.name)
        return case_list

