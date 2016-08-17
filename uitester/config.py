import json
import os
from os.path import pardir

app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), pardir)
config_file = os.path.join(app_dir, 'config')


class Config:

    def __init__(self):
        self.sdk = ''
        self.libs = os.path.abspath(os.path.join(app_dir, 'libs'))
        self.port = 11800

    @classmethod
    def read(cls):
        if not os.path.exists(config_file):
            return Config.make_default_config()
        with json.loads(open(config_file, 'r')) as conf_json:
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

    def update(self):
        pass

    def save(self):
        pass


