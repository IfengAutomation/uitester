import unittest
import os
from uitester import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir)
        self.conf_path = os.path.join(self.root_dir, 'config')

    def test_config_path(self):
        self.assertEqual(os.path.abspath(config.config_file), os.path.abspath(self.conf_path))

    def test_make_default_conf(self):
        if os.path.exists(self.conf_path):
            os.remove(self.conf_path)
        conf = config.Config.make_default_config()
        self.assertEqual(conf.sdk, '')
        self.assertEqual(conf.libs, os.path.abspath(os.path.join(self.root_dir, 'libs')))
        self.assertEqual(conf.port, 11800)
        self.assertTrue(os.path.exists(self.conf_path))

if __name__ == '__main__':
    unittest.main()
