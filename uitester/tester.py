# coding=utf-8

from threading import Thread

from uitester import cache
from uitester.remote_proxy.proxy import CommonProxy
from uitester.config import Config
from uitester.context import Context
from uitester.error_handler import handle_error, error_handlers

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

    @handle_error
    def devices(self):
        """
        show registered devices
        :return:
        """
        return cache.devices

    @handle_error
    def select_devices(self, select_devices):
        """
        select devices for test
        :param select_devices:
        :return:
        """
        pass

    @handle_error
    def execute_script(self, file_name):
        """
        Execute kw script.
        :return:
        """
        proxy = CommonProxy()
        file = open(file_name, encoding='utf-8')
        for line in file:
            name_and_agr_split_index = line.find(' ')  # 方法与参数之间分隔符：空格
            if name_and_agr_split_index == -1:
                kw_name = line.strip()
                kw_args = []
            else:
                kw_name = line[0:name_and_agr_split_index].strip()
                kw_args = line[name_and_agr_split_index:].strip().split('#')  # 多个参数时，参数之间分隔符：#
                kw_args = list(filter(lambda x: x != '', kw_args))
            print("kw_name:{}, args:{}".format(kw_name, kw_args))
            devices = self.devices()
            proxy.proxy_manager(devices, kw_name.lower(), *kw_args)
        proxy.manage_device()

    @handle_error
    def execute_line(self, kw_name, *args):
        """
        Execute kw line
        :return:
        """
        proxy = CommonProxy()
        devices = self.devices()
        proxy.proxy_manager(devices, kw_name.lower(), *args)
        proxy.manage_device()

    @handle_error
    def load_library(self):
        """
        Load kw library write by py
        :return:
        """
        pass

    @handle_error
    def get_kw_info(self, name=None, name_startswith=None):
        """
        get kw help
        :param name: kw name
        :param name_startswith: find kw name by str
        :return:
        """
        pass

    @handle_error
    def get_registered_devices(self):
        """
        get all registered devices
        :return:
        """
        pass

    @handle_error
    def start(self):
        """
        Start RPC-Server in new thread
        :return:
        """
        self.server = rpc_server.get_server('0.0.0.0', 11800)
        Thread(target=self.server.serve_forever, daemon=True).start()

    @handle_error
    def stop(self):
        if self.server:
            self.server.shutdown()



class DefaultErrorHandler:
    def handle(self, e):
        logger.exception(e)
