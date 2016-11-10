from keywords import keyword, new, call, call_static, RemoteObject, RemoteClass

instrument_registry = 'android.support.test.InstrumentationRegistry'
solo_class_name = 'com.robotium.solo.Solo'


class Intent(RemoteObject):
    pass


class Context(RemoteObject):

    def get_package_manager(self):
        obj = call(self, 'getPackageManager')
        return PackageManager.from_object(obj)


class Activity(RemoteObject):
    pass


class PackageManager(RemoteObject):

    def get_launch_intent_for_package(self, package_name):
        obj = call(self, 'getLaunchIntentForPackage', package_name)
        return Intent.from_object(obj)


class Instrumentation(RemoteObject):

    def start_activity_sync(self, intent):
        obj = call(self, 'startActivitySync', intent)
        return Activity.from_object(obj)

    def get_context(self):
        obj = call(self, 'getContext')
        return Context.from_object(obj)

    def get_target_context(self):
        obj = call(self, 'getTargetContext')
        return Context.from_object(obj)


class InstrumentationRegistry(RemoteClass):

    @staticmethod
    def get_instrumentation():
        instrument_registry_class = RemoteClass.from_class_name(instrument_registry)
        remote_obj = call_static(instrument_registry_class, "getInstrumentation")
        return Instrumentation.from_object(remote_obj)


class Solo(RemoteObject):

    def __init__(self, instrumentation):
        solo_class = RemoteClass.from_class_name(solo_class_name)
        instrumentation.class_name = 'android.app.Instrumentation'
        remote_solo = new(solo_class, instrumentation)
        self.__dict__ = remote_solo.__dict__

    def get_view(self, res_id=None, class_name=None):
        if res_id:
            return call(self, "getView", res_id)
        if class_name:
            return call(self, "getView", RemoteClass.from_class_name(class_name))


@keyword("runReflection")
def run_reflection_test():
    instrumentation = InstrumentationRegistry.get_instrumentation()
    intent = instrumentation\
        .get_context()\
        .get_package_manager()\
        .get_launch_intent_for_package("com.ifeng.at.testagent")
    activity = instrumentation.start_activity_sync(intent)
    print(activity.class_name)
    solo = Solo(InstrumentationRegistry.get_instrumentation())
    v = solo.get_view(res_id="com.ifeng.at.testagent:id/email_sign_in_button")
    print(v)


