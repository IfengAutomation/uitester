from uitester.json_rpc.request import Request


class CommonProxy:
    target_devices = []

    def send_msg_to_devices(self, request):
        for device in self.target_devices:
            device.send_msg(request)

    def get_view(self, view_id):
        request = Request(0, "GetView", [view_id])
        self.send_msg_to_devices(request)

    def start_app(self, package_name):
        request = Request(1, "StartMainActivity", [package_name])
        self.send_msg_to_devices(request)

    def finish_app(self):
        request = Request(2, "FinishActivity", [])
        self.send_msg_to_devices(request)

    def click_on_text(self, text):
        request = Request(3, "ClickOnText", [text])
        self.send_msg_to_devices(request)

    def enter_text(self, var, text):
        request = Request(4, "EnterText", [text], var=var)
        self.send_msg_to_devices(request)

    def wait_for_text(self, text):
        request = Request(5, "WaitForText", [text])
        self.send_msg_to_devices(request)
