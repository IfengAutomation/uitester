import unittest
import os
from uitester.device_manager import device_manager
from uitester.device_manager.device import Device


class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        tests_root = os.path.join(os.path.dirname(__file__), os.path.pardir)
        sdk_path = os.path.join(tests_root, 'android_tools/sdk_mock')
        self.context = type('Context', (), {'config': None})()
        config = type('Config', (), {'sdk': '', 'libs': '', 'port': 11800})()
        config.sdk = sdk_path
        self.context.config = config

    def test_get_devices(self):
        dm = device_manager.DeviceManager(self.context)
        devices = dm.devices
        self.assertTrue(len(devices) > 0)
        self.assertTrue(devices[0].id == 'TA09004MPY')
        self.assertTrue(devices[0].status == Device.ONLINE)

    def test_update_devices(self):
        dm = device_manager.DeviceManager(self.context)
        for _ in range(3):
            dm.devices
        devices = dm.devices
        self.assertTrue(len(devices) == 2)
        self.assertTrue(devices[0].id == 'TA09004MPY')
        self.assertTrue(devices[0].status == Device.ONLINE)
