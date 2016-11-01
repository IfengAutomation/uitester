import os


_script_path = os.path.abspath(__file__)

test_manager_dir = os.path.abspath(os.path.join(_script_path, os.path.pardir))

uitester_dir = os.path.abspath(os.path.join(test_manager_dir, os.path.pardir))

root_dir = os.path.abspath(os.path.join(uitester_dir, os.path.pardir))

win_adb = os.path.abspath(os.path.join(root_dir, 'adb/windows/adb.exe'))

osx_adb = os.path.abspath(os.path.join(root_dir, 'adb/osx/adb'))

agent_apk = os.path.abspath(os.path.join(root_dir, 'apk/agent.apk'))
