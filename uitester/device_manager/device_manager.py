from uitester.android_tools.adb import ADB
from uitester.json_rpc import rpc_server
from threading import Thread
from .device import Device


class DeviceManager:
    """
    DeviceManager:
    Create a device instance for every android devices
    Use device instance to execute scripts
    """
    def __init__(self, context):
        self.context = context
        self.__devices = []
        self.server = None
        self.server_thread = None
        self.adb = ADB(context)

    @property
    def devices(self):
        self.update_devices()
        return self.__devices

    def update_devices(self):
        """
        update android devices by adb
        :return:
        """
        self.adb.update()
        device_info_list = self.adb.devices()

        new_devices = []
        for origin_device in device_info_list:
            not_found_in_devices = True
            # if device in devices list, then update status
            for device in self.__devices:
                if origin_device[0] == device.id:
                    status = self.device_status_from_adb(origin_device[1])
                    if status == Device.OFFLINE:
                        device.status = status
                    elif status == Device.ONLINE and device.status == Device.OFFLINE:
                        device.status = status
                    new_devices.append(device)
                    not_found_in_devices = False
                    break
            # if device is new added. make new device instance
            if not_found_in_devices:
                device = Device(origin_device[0])
                device.status = self.device_status_from_adb(origin_device[1])
                new_devices.append(device)
        # set new devices list
        self.__devices = new_devices

    def device_status_from_adb(self, origin_status):
        if origin_status == 'device':
            return Device.ONLINE
        else:
            return Device.OFFLINE

    def start_rpc_server(self):
        self.server = rpc_server.get_server('0.0.0.0', self.context.config.port)
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



