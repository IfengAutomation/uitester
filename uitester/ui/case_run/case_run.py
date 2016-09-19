# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QMessageBox

from uitester.case_manager.database import DBCommandLineHelper
from uitester.kw.kw_runner import KWCase
from uitester.ui.case_run.add_case import AddCaseWidget
from uitester.ui.case_run.add_device import AddDeviceWidget
from uitester.ui.case_run.case_run_status_listener import CaseRunStatusListener
from uitester.ui.case_run.table_widget import RunnerTableWidget


class RunWidget(QWidget):
    running = False
    device_list_signal = pyqtSignal(list, name="device_list_signal")
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

        self.add_case_widget = None
        self.add_device_widget = AddDeviceWidget()
        self.add_device_widget.setWindowModality(Qt.ApplicationModal)

        self.case_widget = RunnerTableWidget([], [0])
        self.case_table_layout.insertWidget(0, self.case_widget)

        self.add_device_widget.add_log_signal.connect(self.add_log, Qt.QueuedConnection)
        self.add_device_widget.run_signal.connect(self.run_case, Qt.QueuedConnection)
        self.device_list_signal.connect(self.add_device_widget.add_radio_to_widget, Qt.QueuedConnection)

    def click_add_case(self):
        """
        click the button to show add case widget
        :return:
        """
        self.add_case_widget = AddCaseWidget()
        self.add_case_widget.select_case_signal.connect(self.show_cases, Qt.QueuedConnection)
        self.add_case_widget.setWindowModality(Qt.ApplicationModal)
        self.add_case_widget.show()

    def click_run_stop_btn(self):
        """
        start or stop to run case
        :return:
        """
        devices = []
        if self.running:
            self.stop_case()
            return
        if not self.cases:  # cases is null
            self.message_box.warning(self, "Message", "Please add cases first.", QMessageBox.Ok)
            return
        if self.tester.devices():
            devices = self.tester.devices()
        self.add_device_widget.show()
        self.device_list_signal.emit(devices)

    def add_log(self, log_info):
        """
        add log to logarea
        :return:
        """
        if self.logarea is None:
            return
        self.logarea.append(log_info)

    def update_case_name_color(self, msg):
        """
        update case's font color according to the case's result
        pass: green; fail: red
        :param msg:
        :return:
        """
        for row_index in range(self.case_widget.dataTableWidget.rowCount()):
            case_id_item = self.case_widget.dataTableWidget.item(row_index, 1)  # get case id from dataTableWidget
            if case_id_item.text() != str(msg.case_id):
                continue
            self.case_widget.dataTableWidget.selectRow(row_index)
            if msg.status == 101:  # case pass
                self.update_green(row_index)
            elif msg.status == 500:
                self.update_red(row_index)
                self.add_log("<pre><font color='red'>" + str(msg.message) + "</font></pre>")
            elif msg.status == 2:
                self.stop_case()

    def run_case(self, devices):
        kw_case_list = []
        if not self.cases:
            return
        for case_id in self.cases:
            kw_case = KWCase()
            case = self.dBCommandLineHelper.query_case_by_id(case_id)
            kw_case.id = case.id
            kw_case.name = case.name
            kw_case.content = case.content
            kw_case_list.append(kw_case)
        # set icon
        stop_icon = QIcon()
        stop_icon.addPixmap(QPixmap(self.config.images + '/stop.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(stop_icon)
        self.run_stop_btn.setText("Stop")
        self.running = True
        try:
            self.tester.start_server()    # start rpc server
        except Exception as e:
            self.add_log(str(e))
        if not devices:
            return
        self.tester.select_devices(devices)
        status_listener = CaseRunStatusListener()
        status_listener.listener_msg_signal.connect(self.update_case_name_color, Qt.QueuedConnection)
        self.tester.add_run_status_listener(status_listener)
        try:
            self.tester.run(kw_case_list)
        except Exception as e:
            self.add_log(str(e))

    def stop_case(self):
        run_icon = QIcon()
        run_icon.addPixmap(QPixmap(self.config.images + '/run.png'), QIcon.Normal, QIcon.Off)
        self.run_stop_btn.setIcon(run_icon)          # change icon
        self.run_stop_btn.setText("Run")
        self.running = False
        try:
            self.tester.stop()
            self.tester.stop_server()
        except Exception as e:
            self.add_log(str(e))

    def show_cases(self, id_list):
        """
        show cases in RunnerTableWidget according to id list
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

    def update_green(self, row_index):
        """
        update item text color to green by row number
        :param row_index:
        :return:
        """
        brush_green_color = QBrush(QColor(55, 177, 88))
        for column_index in range(self.case_widget.dataTableWidget.columnCount()):
            item = self.case_widget.dataTableWidget.item(row_index, column_index)
            item.setForeground(brush_green_color)

    def update_red(self, row_index):
        """
        update item text color to red by row number
        :param row_index:
        :return:
        """
        brush_red_color = QBrush(QColor(255, 0, 0))
        for column_index in range(self.case_widget.dataTableWidget.columnCount()):
            item = self.case_widget.dataTableWidget.item(row_index, column_index)
            item.setForeground(brush_red_color)

