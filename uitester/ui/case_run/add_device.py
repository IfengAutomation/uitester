# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QMessageBox, QRadioButton


class AddDeviceWidget(QWidget):
    add_device_signal = pyqtSignal(str, name="add_device_signal")
    add_log_signal = pyqtSignal(str, name="add_log_signal")
    run_signal = pyqtSignal(list, name="run_signal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_radios = []

        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_device.ui')
        uic.loadUi(ui_file_path, self)

        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 6, screen.height() / 6)

        self.select_device_btn.clicked.connect(self.handle_radio)
        self.cancel_device_btn.clicked.connect(self.close)
        self.message_box = QMessageBox()
        self.devices_list = []

    def handle_radio(self):
        """
        handle the select event
        :return:
        """
        devices = []
        for index in range(len(self.button_radios)):
            item = self.button_radios[index]
            if type(item) == QLabel:
                self.message_box.warning(self, "Message", "Please connect the device to your computer.", QMessageBox.Ok)
                return
            if not item.isChecked():
                self.message_box.warning(self, "Message", "Please choose a device.", QMessageBox.Ok)
                return
            # self.emit_device_info_to_bar(widget.text())  # 主窗口状态栏显示device机身码
            self.emit_log("<font color='black'>Choose device: " + item.text() + " </font>")
            device = self.devices_list[index]
            if device.id == item.text():
                devices.append(device)
            self.run_signal.emit(devices)
            break
        self.close()

    def emit_device_info_to_bar(self, msg):
        """
        send device info signal
        :param msg:
        :return:
        """
        if not msg:
            return
        self.add_device_signal.emit(msg)

    def emit_log(self, msg):
        """
        send log signal
        :param msg:
        :return:
        """
        if not msg:
            return
        self.add_log_signal.emit(msg)

    def add_radio_to_widget(self, devices_list):
        """
        add devices list to "add device" widget
        :param devices_list:
        :return:
        """
        self.clear_button_radios()

        self.devices_list = devices_list
        for device in devices_list:
            radio = QRadioButton(device.id)
            self.button_radios.append(radio)
            self.devices_layout.addWidget(radio)

    def clear_button_radios(self):
        """
        clear the content of devices_layout
        :return:
        """
        for item in self.button_radios:
            item.setParent(None)
        self.button_radios = []

