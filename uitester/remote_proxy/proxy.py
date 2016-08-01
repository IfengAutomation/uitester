from uitester.json_rpc.request import Request


class CommonProxy:
    target_devices = []

    def send_msg_to_devices(self, request):
        for device in self.target_devices:
            device.send_msg(request)

    def get_view(self, view_id):
        request = Request()
        request.id = 0
        request.method = "GetView"
        request.args = [view_id]
        self.send_msg_to_devices(request)

    def start_app(self, package_name):
        request = Request()
        request.id = 1
        request.method = "StartMainActivity"
        request.args = [package_name]
        self.send_msg_to_devices(request)

    def finish_app(self):
        request = Request()
        request.id = 2
        request.method = "FinishActivity"
        self.send_msg_to_devices(request)

    def click_on_text(self, text):
        request = Request()
        request.id = 3
        request.method = "ClickOnText"
        request.args = [text]
        self.send_msg_to_devices(request)

    def enter_text(self, var, text):
        request = Request()
        request.id = 4
        request.method = "EnterText"
        request.args = [text]
        request.var = var
        self.send_msg_to_devices(request)

    def wait_for_text(self, text):
        request = Request()
        request.id = 5
        request.method = "WaitForText"
        request.args = [text]
        self.send_msg_to_devices(request)
