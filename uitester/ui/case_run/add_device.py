# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QLabel, QMessageBox, QRadioButton

from uitester.ui.case_run import case_run


class AddDeviceWidget(QWidget):
    add_device_signal = pyqtSignal(str)
    add_log_signal = pyqtSignal(str)
    run_signal = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_device.ui')
        uic.loadUi(ui_file_path, self)

        # 设置窗口大小
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 6, screen.height() / 6)

        self.select_device_btn.clicked.connect(self.select_event)
        self.cancel_device_btn.clicked.connect(self.close)

    def select_event(self):

        if not case_run.cases:  # case未选
            # 判断case是否已选，否：提示先选case
            QMessageBox.about(self, "Message", "Please add cases first.")
        else:    # case已选
            self.handle_radio(self.devices_layout)

    def handle_radio(self, layout_name):
        """
        对单选按钮选择结果处理
        :param layout_name:
        :return:
        """
        if layout_name is None:
            return
        while layout_name.count():
            item = layout_name.takeAt(0)
            widget = item.widget()
            if (type(widget) is not QRadioButton) or (not widget.isChecked()):
                QMessageBox.about(self, "Message", "Please choose a device.")
                return
            # self.emit_device_info_to_bar(widget.text())  # 主窗口状态栏显示device机身码
            self.emit_log("Choose device: " + widget.text())
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
        self.clear_devices_layout()  # 清除devices_layout

        # 无设备连接时，提示用户
        if len(devices_list) == 0:
            label = QLabel()
            label.setText("There is no device.")
            self.devices_layout.addWidget(label)
            return
        for device in devices_list:
            radio = QRadioButton(device)
            self.devices_layout.addWidget(radio)

    def clear_devices_layout(self):
        """
        清除指定layout中的所有项
        :return:
        """
        def delete_items(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    elif item.layout() is not None:
                        delete_items(item.layout())
            # for index in reversed(range(layout.count())):
            #     widget = layout.takeAt(index).widget()
            #     if widget is not None:
            #         widget.deleteLater()
        delete_items(self.devices_layout)
