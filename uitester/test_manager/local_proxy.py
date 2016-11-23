import socket
import requests
import json


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


local_ip = get_local_ip()


def _start_app(package_name):
    pass


def _kill_app(package_name):
    pass


def _clear_cache(package_name):
    pass


def _install_apk():
    pass


def _uninstall_package():
    pass


def activate_mock_interface(interface_name):
    r = requests.get('http://'+local_ip+':8080/api/active/'+interface_name+'/true')
    if r.status_code != 200:
        return False
    if r.text.strip() == 'OK':
        return True
    else:
        return False


def deactivate_mock_interface(interface_name):
    r = requests.get('http://'+local_ip+':8080/api/active/'+interface_name+'/false')
    if r.status_code != 200:
        return False
    if r.text.strip() == 'OK':
        return True
    else:
        return False


def reset_mock_interface():
    r = requests.get('http://'+local_ip+':8080/api/reset')
    if r.status_code != 200:
        return False
    if r.text.strip() == 'OK':
        return True
    else:
        return False


def get_request_list():
    r = requests.get('http://'+local_ip+':8080/api/request_list')
    if r.status_code != 200:
        raise ValueError('Get request list failed. status code = '+str(r.status_code))
    return r.json()


def clear_request_list():
    r = requests.get('http://'+local_ip+':8080/api/clear_request_list')
    if r.status_code != 200:
        raise ValueError('Clear request list failed. status code = '+str(r.status_code))
    return r.text.strip() == 'OK'
