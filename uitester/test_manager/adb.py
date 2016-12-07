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


def install(apk_file, device_id=None):
    cmd = [_adb, 'install', '-r', apk_file]
    if device_id:
        cmd.insert(1, '-s')
        cmd.insert(2, device_id)
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    _output = p.stdout.decode()
    if 'Success' in _output:
        return True, _output
    elif 'Failure' in _output:
        return False, _output
    else:
        return False, _output


def uninstall(package_name, device_id=None):
    cmd = [_adb, 'uninstall', package_name]
    if device_id:
        cmd.insert(1, '-s')
        cmd.insert(2, device_id)
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
        '-s',
        device_id,
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

