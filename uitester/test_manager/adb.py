import subprocess
import platform
from uitester.test_manager import path_helper


sys_name = platform.system().lower()
if sys_name == 'windows':
    _adb = path_helper.win_adb
elif sys_name == 'darwin':
    _adb = path_helper.osx_adb
else:
    _adb = 'adb'


def install(apk_file):
    cmd = [_adb, 'install', '-r', apk_file]
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    _output = p.stdout.decode()
    if 'Success' in _output:
        return True, _output
    elif 'Failure' in _output:
        return False, _output
    else:
        return False, _output


def uninstall(package_name):
    cmd = [_adb, 'uninstall', package_name]
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    _output = p.stdout.decode()
    if 'Success' in _output:
        return True, _output
    elif 'Failure' in _output:
        return False, _output
    else:
        return False, _output


def start_agent(host, port, device_id, debug=False, target_package='com.ifeng.at.testagent'):
    is_debug = 'false'
    if debug:
        is_debug = 'true'

    cmd = [
        _adb,
        'shell',
        'am',
        'instrument',
        '-w',
        '-r',
        '-e', 'debug', is_debug,
        '-e', 'host', host,
        '-e', 'port', str(port),
        '-e', 'id', device_id,
        '-e', 'class', 'com.ifeng.at.testagent.Agent#start',
        target_package+'.test/android.support.test.runner.AndroidJUnitRunner']

    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    _output = p.stdout.decode()
    if '\nFAILURES!!!' in _output:
        return False, _output
    elif 'INSTRUMENTATION_STATUS: Error' in _output:
        return False, _output
    else:
        return True, _output


def devices():
    cmd = [
        _adb,
        'devices'
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    _output = p.stdout.decode()
    device_lines = _output.splitlines()
    if len(device_lines) <= 0:
        raise ValueError('Get devices list failed, can\'t read adb log')
    if not device_lines[0].startswith('List'):
        raise ValueError('device list error\n{}'.format(device_lines[0]))

    _devices = {}
    if len(device_lines) > 1:
        for line in device_lines:
            device = line.split('\t')
            if len(device) == 2:
                _devices[device[0].strip()] = device[1].strip()
    return _devices


if __name__ == '__main__':
    res, output = install('/Users/zhaoye/github/uitester/apk/agent.apk')
    print('TEST INSTALL:', res, '\n', output)
    res, output = start_agent('172.30.20.51', 11800, '123')
    print('TEST INSTRUMENT', res, '\n', output)
    res, output = uninstall('com.ifeng.at.testagent.test')
    print('TEST UNINSTALL', res, '\n', output)
    device_list = devices()
    print(device_list)
