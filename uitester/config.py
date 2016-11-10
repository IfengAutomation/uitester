import json
import os
from os.path import pardir

app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), pardir)
config_file = os.path.join(app_dir, 'config')


class Config:
    """
    Config class
    Config.read() read config from json file, return a Config instance
    Config.save() save settings in json file
    """
    def __init__(self):
        self.debug = False
        self.target_package = "com.ifeng.at.testagent"
        self.libs = os.path.abspath(os.path.join(app_dir, 'libs'))
        self.port = 11800
        self.images = os.path.abspath(os.path.join(app_dir, 'images'))

    @classmethod
    def read(cls):
        if not os.path.exists(config_file):
            return Config.make_default_config()
        conf_json = json.loads(open(config_file, 'r').read())
        conf = cls()
        for k in conf_json:
            setattr(conf, k, conf_json[k])
        return conf

    @staticmethod
    def make_default_config():
        conf = Config()
        f = open(config_file, 'w')
        conf_json_str = json.dumps(conf.__dict__, indent=4, ensure_ascii=False)
        f.write(conf_json_str)
        f.close()
        return conf

    @staticmethod
    def clear_config():
        if os.path.exists(config_file):
            os.remove(config_file)

    def save(self):
        conf_str = json.dumps(self.__dict__, ensure_ascii=False, indent=4)
        if not os.path.exists(config_file):
            Config.make_default_config()

        f = open(config_file, 'w')
        f.write(conf_str)
        f.close()


