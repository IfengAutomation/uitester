# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QMessageBox, QRadioButton, QVBoxLayout

# from uitester.ui.case_run import case_run


class AddDeviceWidget(QWidget):
    add_device_signal = pyqtSignal(str)
    add_log_signal = pyqtSignal(str)
    run_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.buttons_or_labels = []
        self.cases = []

        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_device.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 6, screen.height() / 6)

        self.select_device_btn.clicked.connect(self.select_event)
        self.cancel_device_btn.clicked.connect(self.close)

    def select_event(self):

        if not self.cases:  # case未选
            # 判断case是否已选，否：提示先选case
            QMessageBox.about(self, "Message", "Please add cases first.")
        else:    # case已选
            self.handle_radio()

    def handle_radio(self):
        """
        对单选按钮选择结果处理
        :param layout_name:
        :return:
        """
        for index in range(len(self.buttons_or_labels)):
            item = self.buttons_or_labels[index]
            if type(item) == QLabel:  # 无设备连接提示
                QMessageBox.about(self, "Message", "Please connect the device to your computer.")
                return
            if not item.isChecked():  # 有设备但未选提示
                QMessageBox.about(self, "Message", "Please choose a device.")
                return
            # self.emit_device_info_to_bar(widget.text())  # 主窗口状态栏显示device机身码
            self.emit_log("Choose device: " + item.text())
            self.run_signal.emit()   # 发送run signal
        self.close()
        # TODO 执行注册、执行case

    def emit_device_info_to_bar(self, msg):
        """
        发送device info signal
        :param msg:
        :return:
        """
        if not msg:
            return
        self.add_device_signal.emit(msg)

    def emit_log(self, msg):
        """
        发送log signal
        :param msg:
        :return:
        """
        if not msg:
            return
        self.add_log_signal.emit(msg)

    def add_radio_to_widget(self, devices_list, cases_list):
        """
        将devices_list以单选框的形式展示在页面中
        :param cases_list:
        :param devices_list:
        :return:
        """
        self.clear_button_or_label()  # 清除devices_layout中记录
        self.cases = cases_list

        # 无设备连接时，提示用户
        if len(devices_list) == 0:
            label = QLabel()
            label.setText("There is no device.")
            self.buttons_or_labels.append(label)
            self.devices_layout.addWidget(label)
            return
        for device in devices_list:
            # radio = QRadioButton(device)
            radio = QRadioButton(device.id)
            self.buttons_or_labels.append(radio)
            self.devices_layout.addWidget(radio)

    def clear_button_or_label(self):
        """
        清除单选项或提示label
        :return:
        """
        for item in self.buttons_or_labels:
            item.setParent(None)
        self.buttons_or_labels = []

