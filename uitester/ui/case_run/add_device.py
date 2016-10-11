# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox, QRadioButton

from uitester.test_manager.device_manager import Device


class AddDeviceWidget(QWidget):
    add_log_signal = pyqtSignal(str, name="add_log_signal")
    run_case_signal = pyqtSignal(list, name="run_signal")
    run_editor_signal = pyqtSignal(list, int, name="run_editor_signal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.devices_radio_buttons = []
        self.data_count = None
        self.selected_data_number = 0  # init data number, '0' refer to all data
        self.selected_device_list = []

        ui_dir_path = os.path.dirname(__file__)
        ui_file_path = os.path.join(ui_dir_path, 'add_device.ui')
        uic.loadUi(ui_file_path, self)

        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 6, screen.height() / 6)

        self.all_data_selected = True
        self.line_number_line_edit.hide()

        self.select_device_btn.clicked.connect(self.select_event)
        self.cancel_device_btn.clicked.connect(self.close)
        self.all_radio_btn.clicked.connect(self.data_all_radio_event)
        self.line_number_radio_btn.clicked.connect(self.data_specified_radio_event)

        self.message_box = QMessageBox()
        self.devices_list = []

    def select_event(self):
        """
        handle the select event
        :return:
        """
        self.handle_selected_device()
        if not self.selected_device_list:  # no device is selected
            self.message_box.warning(self, "Message", "Please choose a device.", QMessageBox.Ok)
            return

        # case data handle
        if not self.all_data_selected:
            input_number = self.line_number_line_edit.text().strip()
            if not input_number or (not input_number.isdigit()):
                self.message_box.warning(self, "Message", "Please input the right line number.", QMessageBox.Ok)
                return
            if not (0 < int(input_number) <= self.data_count):
                self.message_box.warning(self, "Message", "Please input the right line number.", QMessageBox.Ok)
                return
            self.selected_data_number = int(input_number)
        if self.data_count is None:
            # case run
            self.run_case_signal.emit(self.selected_device_list)
            self.close()
            return

        # editor run
        self.run_editor_signal.emit(self.selected_device_list, self.selected_data_number)
        self.close()

    def handle_selected_device(self):
        """
        handle selected device
        :return:
        """
        for index in range(len(self.devices_radio_buttons)):
            item = self.devices_radio_buttons[index]
            if not item.isChecked():
                continue
            self.emit_log("<font color='black'>Choose device: " + item.text() + " </font>")
            for device in self.devices_list:
                if device.id == item.text().strip().split(" (")[0]:
                    self.selected_device_list.append(device)
            break

    def data_specified_radio_event(self):
        """
        handle the specified_radio's click event
        :return:
        """
        if self.line_number_radio_btn.isChecked():
            self.all_data_selected = False
            if self.data_count == 1:
                message = "Enter an integer: 1"
            else:
                message = "Enter an integer in range: 1 - " + str(self.data_count)
            self.line_number_line_edit.setPlaceholderText(message)
            self.line_number_line_edit.show()

    def data_all_radio_event(self):
        """
        handle the all_radio_btn's click event
        :return:
        """
        if self.all_radio_btn.isChecked():
            self.all_data_selected = True
            self.line_number_line_edit.hide()

    def emit_log(self, msg):
        """
        send log signal
        :param msg:
        :return:
        """
        if not msg:
            return
        self.add_log_signal.emit(msg)

    def add_radio_to_widget(self, devices_list, data_count=None):
        """
        add devices list to "add device" widget
        :param data_count:
        :param devices_list:
        :return:
        """
        self.clear_devices_radio_btn()

        self.devices_list = devices_list
        for device in devices_list:
            radio = QRadioButton(device.id + " (" + device.description + ")")
            if device.status != Device.ONLINE:
                radio.setDisabled(True)
            self.devices_radio_buttons.append(radio)
            self.devices_layout.addWidget(radio)

        if data_count is None:  # Case Run
            self.data_area.setEnabled(False)
            self.data_area.hide()
            return
        if data_count == 0:  # editor run and data count is 0
            self.data_area.setEnabled(False)
            self.data_area.hide()
        self.data_area.setEnabled(True)
        self.data_count = data_count

    def clear_devices_radio_btn(self):
        """
        clear the content of devices_layout
        :return:
        """
        for item in self.devices_radio_buttons:
            item.setParent(None)
        self.devices_radio_buttons = []

