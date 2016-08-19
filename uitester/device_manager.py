from uitester.android_tools.adb import ADB
from uitester.json_rpc import rpc_server
from threading import Thread


class DeviceManager:
    """
    DeviceManager:
    Create a device instance for every android devices
    Use device instance to execute scripts
    """
    def __init__(self, context):
        self.context = context
        self.devices = []
        self.server = None
        Thread(target=self.update_devices, daemon=True).start()

    def update_devices(self):
        """
        update android devices by adb
        :return:
        """
        while True:
            # TODO check adb devices, update devices
            pass

    def restart_rpc_server(self):
        """
        restart rpc socket server
        :return:
        """
        if self.server:
            self.server.shutdown()
            self.server = None

        self.server = rpc_server.get_server('0.0.0.0', self.context.config.port)
        Thread(target=self.server.serve_forever(1), daemon=True).start()



