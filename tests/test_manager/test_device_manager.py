import unittest
from uitester.test_manager import device_manager


class DeviceManagerTest(unittest.TestCase):

    def test_device(self):
        device = device_manager.Device('device-id')
        device.status = device_manager.Device.ONLINE
        self.assertTrue(device.id == 'device-id')
        self.assertTrue(device.status == device_manager.Device.ONLINE)
        self.assertTrue(device.description == device_manager.Device.ONLINE[1])
