from threading import Thread
from uitester.json_rpc import rpc_server


class Tester:
    """
    UI Tester main class.
    Delegate all function here.
    UI and CMD should use this class.
    """
    def __init__(self):
        self.server = None

    def execute_script(self):
        """
        Execute kw script.
        :return:
        """
        pass

    def execute_line(self):
        """
        Execute kw line
        :return:
        """
        pass

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
        self.server = rpc_server.get_server('localhost', 11800)
        Thread(target=self.server.serve_forever, daemon=True).start()

    def stop(self):
        if self.server:
            self.server.shutdown()


