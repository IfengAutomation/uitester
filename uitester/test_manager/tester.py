# coding=utf-8

import logging

from uitester.config import Config
from uitester.error_handler import handle_error, error_handlers
from uitester.test_manager.kw_runner import KWRunner, KWDebugRunner
from uitester.test_manager.context import Context
from uitester.test_manager.device_manager import DeviceManager


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Tester')
logger.setLevel(logging.DEBUG)


class Tester:
    """
    UI Tester main class.
    Delegate all function here.
    UI and CMD should use this class.
    """
    def __init__(self):
        self.conf = Config.read()
        self.context = Context()
        setattr(self.context, 'config', self.conf)
        error_handlers.append(DefaultErrorHandler())
        self.dm = DeviceManager(self.context)
        self.selected_device = None
        self.runner = KWRunner(device_manager=self.dm)

    @handle_error
    def get_config(self):
        return self.conf

    @handle_error
    def devices(self):
        """
        show registered devices
        :return:
        """
        return self.dm.devices

    @handle_error
    def select_devices(self, devices):
        """
        select devices for test
        :param devices:
        :return:
        """
        self.dm.selected_devices = devices

    @handle_error
    def add_run_status_listener(self, status_listener):
        self.runner.listener = status_listener

    @handle_error
    def run(self, cases):
        self.runner.execute(cases, self.dm.selected_devices)

    @handle_error
    def stop(self):
        self.runner.stop()

    @handle_error
    def get_debug_runner(self):
        return KWDebugRunner(self.dm)

    @handle_error
    def start_server(self):
        """
        Start RPC-Server in new thread
        :return:
        """
        self.dm.start_rpc_server()

    @handle_error
    def stop_server(self):
        pass

    @handle_error
    def install_agent(self):
        pass

    @handle_error
    def start_agent(self):
        pass


class DefaultErrorHandler:
    def handle(self, e):
        logger.exception(e)
