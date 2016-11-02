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
        self._devices = {}
        self._selected_devices = []
        self.server = None
        self.server_thread = None
        self.msg_queue = Queue()

    @property
    def selected_devices(self):
        self.update_devices()
        return self._selected_devices

    @selected_devices.setter
    def selected_devices(self, devices):
        self._selected_devices = devices

    @property
    def devices(self):
        self.update_devices()
        return list(self._devices.values())

    def update_devices(self):
        """
        update android devices by adb
        :return:
        """
        devices_info = adb.devices()

        # update device status
        for device_id in devices_info:
            device_status = devices_info[device_id]
            if device_id not in self._devices:
                self._devices[device_id] = Device(device_id)
            self._update_device_status(self._devices[device_id], device_status)

        # remove not exist device
        for device_id in self._devices:
            if device_id not in devices_info:
                self._devices.pop(device_id)

    def _update_device_status(self, device, device_status):
        if device_status == 'device':
            agent = self.server.get_agent(device.id)
            if agent:
                device.agent = agent
            device.status = Device.ONLINE
        else:
            device.status = Device.OFFLINE

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

