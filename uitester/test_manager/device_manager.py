from uitester.test_manager import adb
from uitester.test_manager import rpc_server
from threading import Thread
from queue import Queue


class Device:
    BLANK = 0x0, 'Default status'
    OFFLINE = 0x1, 'Device is offline'
    ONLINE = 0x2, 'Device is online'
    RUNNING = 0x3, 'Device is running tests'

    def __init__(self, device_id):
        self.status = self.BLANK
        self.id = device_id
        self.agent = None

    @property
    def description(self):
        return self.status[1]


class DeviceManager:
    """
    DeviceManager:
    Create a device instance for every android devices
    Use device instance to execute scripts
    """
    def __init__(self, context):
        self.context = context
        self.__devices = []
        self.selected_devices = []
        self.server = None
        self.server_thread = None
        self.msg_queue = Queue()

    @property
    def devices(self):
        self.update_devices()
        return self.__devices

    def update_devices(self):
        """
        update android devices by adb
        :return:
        """
        device_info_list = adb.devices()

        new_devices = []
        for device_info in device_info_list:
            device = Device(device_info[0])
            if device_info[1].strip() == 'device':
                agent = self.server.get_agent(device.id)
                if agent:
                    device.agent = agent
                device.status = Device.ONLINE
            else:
                device.status = Device.OFFLINE
            new_devices.append(device)
        self.__devices = new_devices

    def start_rpc_server(self):
        self.server = rpc_server.get_server(self.context.config.port)
        self.server_thread = Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def restart_rpc_server(self):
        """
        restart rpc socket server
        :return:
        """
        if self.server:
            self.server.shutdown()
            self.server = None
        if self.server_thread:
            self.server_thread = None
        self.start_rpc_server()

