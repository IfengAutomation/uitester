# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QHBoxLayout, QRadioButton


class AddDeviceWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_device.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 5 * 2, screen.height() / 5 * 2)

        devices_list = self.list_devices()   # 列出所有已连接的devices
        self.add_radio_to_widget(devices_list)  # 将devices_list以单选框的形式展示在页面中

        self.select_device_btn.clicked.connect(self.select_event)
        self.cancel_device_btn.clicked.connect(self.cancel_event)

    def select_event(self):
        # TODO 选择结果传递，返回Run页面
        pass

    def cancel_event(self):
        self.close()

    def list_devices(self):
        """
        通过adb命令获取当前连接的device
        :return:
        """
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

    def add_radio_to_widget(self, devices_list):
        """
        将devices_list以单选框的形式展示在页面中
        :param devices_list:
        :return:
        """
        device_box_layout = QHBoxLayout()
        for device in devices_list:
            radio = QRadioButton(device)
            if devices_list.index(device) == 0:  # 默认第一个单选框选中状态
                radio.setChecked(True)
            device_box_layout.addWidget(radio)
        self.devices.setLayout(device_box_layout)

