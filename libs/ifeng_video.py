from keywords import keyword, RemoteObject, get_local_ip
from solo import InstrumentationRegistry

data_interface_class_name = "com.ifeng.video.dao.db.constants.DataInterface"
FIELD_VCIS = "HTTP_VCIS_IFENG_COM"
FIELD_VCSP = "HTTP_VCSP_IFENG_COM"
FIELD_V = "HTTP_V_IFENG_COM"
FIELD_COMMENT = "HTTP_COMMENT_IFENG_COM"


@keyword("set_host")
def set_host():
    host = get_local_ip() + ':8080'
    data_interface = RemoteObject.from_class_name(data_interface_class_name)
    data_interface.set_field(FIELD_VCIS, host)
    data_interface.set_field(FIELD_VCSP, host)
    data_interface.set_field(FIELD_COMMENT, host)
    data_interface.set_field(FIELD_V, host)


@keyword("start_video")
def start_ifengvideo():
    instrumentation = InstrumentationRegistry.get_instrumentation()
    intent = instrumentation \
        .get_target_context() \
        .get_package_manager() \
        .get_launch_intent_for_package("com.ifeng.newvideo")
    activity = instrumentation.start_activity_sync(intent)


@keyword("wait")
def wait_debug():
    import time
    time.sleep(120)
