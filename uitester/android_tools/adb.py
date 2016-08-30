import base64
import os
import platform

import subprocess
from threading import Thread


class ADBError(ValueError):
    pass


class ADB:

    """ADB"""

    def __init__(self, context):
        self.context = context
        self.sdk_path = None
        self.appt_path = None
        self.adb_path = None
        self.__logcat_process = None

    def update(self):
        self.sdk_path = sdk_path = self.context.config.sdk
        if platform.system() == 'Windows':
            self.adb_path = os.path.join(sdk_path, 'platform-tools\\adb.exe')
            build_tool_parent_dir = os.path.join(sdk_path, 'build-tools')
            dirs = os.listdir(build_tool_parent_dir)
            for dirName in dirs:
                tool_dir = os.path.join(build_tool_parent_dir, dirName)
                if os.path.isfile(tool_dir):
                    continue
                else:
                    self.appt_path = os.path.join(tool_dir, 'aapt.exe')
                    break
        else:
            self.adb_path = os.path.join(sdk_path, 'platform-tools/adb')
            build_tool_parent_dir = os.path.join(sdk_path, 'build-tools')
            dirs = os.listdir(build_tool_parent_dir)
            for dirName in dirs:
                tool_dir = os.path.join(build_tool_parent_dir, dirName)
                if os.path.isfile(tool_dir):
                    continue
                else:
                    self.appt_path = os.path.join(tool_dir, 'aapt')
                    break

    def install(self, apk_path):
        """
        Install apk
        """
        print('ADB: begin install ' + apk_path)
        cmd = '%s install -r %s' % (self.adb_path, apk_path)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        out, error = p.communicate()
        lines = out.splitlines()
        for line in lines:
            if 'Success' in line:
                print('ADB: install success')
                return True, line
            if 'Failure' in line:
                print('ADB: install failed. ' + line[len('False'):])
                return False, line
        return False, None

    def instrument(self, test_package_name, runner='android.support.test.runner.AndroidJUnitRunner',
                   case_classes=None, params=None):
        """
        run instrument test, and write junit log into log_file.
        """
        if params is None:
            params = {}
        if case_classes is None:
            case_classes = []
        print('ADB: instrument start')
        case_param = ''
        if len(case_classes) > 0:
            case_param = '-e class '
            for case in case_classes:
                if len(case_param) > len('-e class '):
                    case_param += ','
                case_param += case
        if len(params) > 0:
            for k in params:
                case_param += ' -e {} {}'.format(k, params[k])
        # print 'ADB: case_param = ' + case_param
        cmd = '%s shell am instrument -w -r %s %s/%s ' % (self.adb_path, case_param, test_package_name, runner)
        # print 'ADB:cmd before encode = ' + cmd
        # print 'ADB: Run cmd = ' + cmd
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        out, err = p.communicate()
        print('ADB: instrument stop')
        return True, out

    def uninstall(self, package_name):
        """
        uninstall by package name
        """
        print('ADB: uninstall ' + package_name)
        cmd = '%s uninstall %s' % (self.adb_path, package_name)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

    def devices(self):
        """
        show devices
        :return [['id', 'status']...]
        """
        cmd = '%s devices' % (self.adb_path,)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        out, error = p.communicate()
        device_lines = out.splitlines()
        if len(device_lines) <= 0:
            raise ADBError(error)
        if not device_lines[0].startswith('List'):
            raise ADBError('device list error\n{}'.format(device_lines[0]))

        devices = []
        if len(device_lines) > 1:
            for line in device_lines:
                device = line.split('\t')
                if len(device) == 2:
                    devices.append(device)
        return devices

    def package_name(self, apk_path):
        """
        read package name use aapt
        """
        # execute "aapt d badging [apk_file_path]"
        cmd = '%s d badging %s' % (self.appt_path, apk_path)
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out, error = p.communicate()
        lines = out.splitlines()
        # print lines[0]
        # get 'name='package name' value'
        pkg_name_start_index = lines[0].find('name=\'') + 6
        pkg_name_end_index = lines[0][pkg_name_start_index:].find('\'')
        # print 'get sub str from %d to %d' % (pkg_name_start_index, pkg_name_start_index + pkg_name_end_index)
        return lines[0][pkg_name_start_index:pkg_name_start_index + pkg_name_end_index]

    def logcat(self, log_file):
        cmd = '%s logcat -c' % (self.adb_path,)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()
        self.__logcat_process = p = subprocess.Popen(
            '%s logcat -v time' % (self.adb_path,), shell=True, stdout=subprocess.PIPE)
        thread = Thread(target=self.__handle_output, args=(p, log_file))
        thread.start()

    def stop_logcat(self):
        if self.__logcat_process is not None:
            self.__logcat_process.kill()
            self.__logcat_process = None

    def pm_clear(self, packagename):
        cmd = '%s shell pm clear %s' % (self.adb_path, packagename)
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

    def get_sys_prop(self, output_file):
        cmd = '%s shell getprop' % (self.adb_path,)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        f = open(output_file, 'a')
        while p.poll() is None:
            line = p.stdout.readline()
            f.write(line)
        f.close()

    def get_meminfo(self, package_name, output_file):
        cmd = '%s shell dumpsys meminfo %s' % (self.adb_path, package_name)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        f = open(output_file, 'a')
        while p.poll() is None:
            line = p.stdout.readline()
            f.write(line)
        f.close()

    def __handle_output(self, p, log_file):
        print('logcat: thread start')
        f = open(log_file, 'a')
        while p.poll() is None:
            line = p.stdout.readline()
            f.write(line)
        print('logcat: thread stop')
        f.close()