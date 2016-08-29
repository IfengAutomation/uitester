# -*- encoding: UTF-8 -*-
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor, QStandardItemModel, QStandardItem
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
        self.add_device_widget.setWindowModality(Qt.ApplicationModal)

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
        self.add_device_widget.show()
        self.device_list_signal.emit(self.list_devices())

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
            data = model.data(index)
            if str(case_id) == str(data):
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
        # TableView 实现
        case_name_model = QStandardItemModel()
        for case_id in id_list:
            case = self.dBCommandLineHelper.query_case_by_id(case_id)
            case_name_model.setItem(id_list.index(case_id), 0, QStandardItem(str(case.id)))  # 每行第一列为id
            case_name_model.setItem(id_list.index(case_id), 1, QStandardItem(case.name))  # 每行第二列为case name

        # 隐藏表头
        self.case_table_view.verticalHeader().hide()
        self.case_table_view.horizontalHeader().hide()

        self.case_table_view.setModel(case_name_model)

        self.case_table_view.resizeColumnsToContents()  # 根据content设置size
        self.case_table_view.setShowGrid(False)   # 不显示网格
        self.case_table_view.setColumnHidden(0, True)  # 隐藏id列

