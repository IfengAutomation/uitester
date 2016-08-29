from uitester.android_tools.adb import ADB
from unittest import TestCase
import os


class AdbTestCase(TestCase):

    def setUp(self):
        sdk_path = os.path.join(os.path.dirname(__file__), 'sdk_mock')
        self.context = type('Context', (), {'config': None})()
        config = type('Config', (), {'sdk': '', 'libs': '', 'port': 11800})()
        config.sdk = sdk_path
        self.context.config = config

    def test_init(self):
        adb = ADB(self.context)
        adb.update()
        devices = adb.devices()
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0], ['TA09004MPY', 'device'])
        self.assertEqual(devices[1], ['TA09004MPA', 'device'])

    def test_install(self):
        adb = ADB(self.context)
        adb.update()
        res, line = adb.install('test-apk-path/something.apk')
        self.assertTrue(res)

    def test_install_fail(self):
        adb = ADB(self.context)
        adb.update()
        res, line = adb.install('fail')
        self.assertFalse(res)

    def test_start_instrument(self):
        adb = ADB(self.context)
        adb.update()
        res, line = adb.instrument('com.ifeng.at.testagent.test',
                                   case_classes='Agent#start',
                                   params={'ip': '172.0.0.1', 'port': 11800, 'id': 'TA09004MPY'})
        self.assertTrue(res)
