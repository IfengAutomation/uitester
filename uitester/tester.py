from threading import Thread

from uitester import cache
from uitester.json_rpc import rpc_server
from uitester.remote_proxy.proxy import CommonProxy


class Tester:
    """
    UI Tester main class.
    Delegate all function here.
    UI and CMD should use this class.
    """
    def __init__(self):
        self.server = None

    def devices(self):
        """
        show registered devices
        :return:
        """
        return cache.devices

    def select_devices(self, select_devices):
        """
        select devices for test
        :param select_devices:
        :return:
        """
        pass

    def execute_script(self, file_name):
        """
        Execute kw script.
        :return:
        """
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
            self.execute_line(kw_name.lower(), *kw_args)

    def execute_line(self, kw_name, *args):
        """
        Execute kw line
        :return:
        """
        proxy = CommonProxy()
        for (id, device) in self.devices().items():
            proxy.target_devices.add(device)
        if kw_name == 'startapp':
            proxy.start_app(args[0])
        elif kw_name == 'waitfortext':
            proxy.wait_for_text(args[0])
        elif kw_name == 'getview':
            proxy.get_view(args[0])
        elif kw_name == 'entertext':
            if cache.entity.get("code"):
                proxy.enter_text(cache.entity.get("code"), args[1])
            # TODO handle 异常，code为空怎么办？？？
        elif kw_name == 'clickontext':
            proxy.click_on_text(args[0])
        elif kw_name == 'clickonview':
            if cache.entity.get("code"):
                proxy.click_on_view(cache.entity.get("code"))
        elif kw_name == 'switchtotab':
            if cache.entity.get("code"):
                proxy.switch_to_tab(cache.entity.get("code"), args[1])
        elif kw_name == 'finishapp':
            proxy.finish_app()

    def load_library(self):
        """
        Load kw library write by py
        :return:
        """
        pass

    def get_kw_info(self, name=None, name_startswith=None):
        """
        get kw help
        :param name: kw name
        :param name_startswith: find kw name by str
        :return:
        """
        pass

    def get_registered_devices(self):
        """
        get all registered devices
        :return:
        """
        pass

    def start(self):
        """
        Start RPC-Server in new thread
        :return:
        """
        self.server = rpc_server.get_server('172.30.22.80', 11800)
        Thread(target=self.server.serve_forever, daemon=True).start()

    def stop(self):
        if self.server:
            self.server.shutdown()


