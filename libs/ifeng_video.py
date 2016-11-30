from common import *
from keywords import RemoteObject, get_local_ip, call_static, set_var
from solo import Solo
from start import *

data_interface_class_name = "com.ifeng.at.testagent.reflect.DataInterfaceHelper"


@keyword("set_host")
def set_host():
    """
    Set Ifeng video request host to local mock server.
    """
    host = get_local_ip()
    data_interface = RemoteObject.from_class_name(data_interface_class_name)
    call_static(data_interface, "setHost", host+':8080/mock')


@keyword("set_proxy")
def set_proxy():
    """
    Set Ifeng video request host to local proxy server.
    """
    host = get_local_ip()
    data_interface = RemoteObject.from_class_name(data_interface_class_name)
    call_static(data_interface, "setHost", host+':8080/proxy')


@keyword("start_video")
def start_ifengvideo():
    """
    Start Ifeng Video app. Add init test var.
    """
    instrumentation = InstrumentationRegistry.get_instrumentation()
    intent = instrumentation \
        .get_target_context() \
        .get_package_manager() \
        .get_launch_intent_for_package("com.ifeng.newvideo")
    activity = instrumentation.start_activity_sync(intent)
    solo = Solo(instrumentation, activity)
    set_var("solo", solo)

    # add ui_device to var_cache
    ui_device = UIDevice.get_instance(instrumentation)
    set_var("ui_device", ui_device)


@keyword("wait")
def wait_debug(wait_time):
    """
    Wait for sec
    :param wait_time: sec
    """
    import time
    time.sleep(int(wait_time))


@keyword("get_host")
def get_host():
    data_interface = RemoteObject.from_class_name("com.ifeng.video.dao.db.constants.DataInterface")
    v = data_interface.get_field("LIVE_CHANNEL_INFO")
    print(v)
