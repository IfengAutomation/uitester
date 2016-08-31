# coding=utf-8

from threading import Thread

from uitester.config import Config
from uitester.context import Context
from uitester.error_handler import handle_error, error_handlers
from uitester.device_manager.device_manager import DeviceManager
from uitester.kw import kw, kw_runner

import logging

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
        self.runner = kw_runner.KWRunner()

    @handle_error
    def devices(self):
        """
        show registered devices
        :return:
        """
        return self.dm.devices

    @handle_error
    def select_devices(self, device):
        """
        select devices for test
        :param device:
        :return:
        """
        self.selected_device = device

    @handle_error
    def add_run_status_listener(self, status_listener):
        self.runner.running_status_listeners.append(status_listener)

    @handle_error
    def run(self, cases):
        self.runner.run(cases)

    @handle_error
    def get_kw_runner(self):
        return kw.KWCore()

    @handle_error
    def start(self):
        """
        Start RPC-Server in new thread
        :return:
        """
        self.dm.start_rpc_server()

    @handle_error
    def stop(self):
        pass


class DefaultErrorHandler:
    def handle(self, e):
        logger.exception(e)
