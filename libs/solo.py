from keywords import keyword, new, call, call_static, RemoteObject, RemoteClass

instrument_registry = 'android.support.test.InstrumentationRegistry'
solo_class_name = 'com.robotium.solo.Solo'


class Solo(RemoteObject):

    @classmethod
    def get_instance(cls):
        instrument_registry_class = RemoteClass.from_class_name(instrument_registry)
        instrument_object = call_static(instrument_registry_class, "getInstrumentation")
        solo_class = RemoteClass.from_class_name(solo_class_name)
        instrument_object.class_name = 'android.app.Instrumentation'
        remote_solo = new(solo_class, instrument_object)
        solo = cls()
        solo.__dict__ = remote_solo.__dict__
        return solo

    def get_view(self, res_id=None, class_name=None):
        if res_id:
            return call(self, "getView", res_id)
        if class_name:
            return call(self, "getView", RemoteClass.from_class_name(class_name))


@keyword("runReflection")
def run_reflection_test():
    solo = Solo.get_instance()
    print(solo)
    print(solo.__dict__)
    v = solo.get_view(res_id="com.ifeng.at.testagent:id/email_sign_in_button")
    print(v)


