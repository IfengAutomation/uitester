from uitester import cache
from uitester.json_rpc.request import Request


class CommonProxy:
    target_devices = set([])

    def send_msg_to_devices(self, request):
        for device in self.target_devices:
            device.init_msg_list(request)

    def manage_device(self):
        for device in self.target_devices:
            device.msg_manager()

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
        cache.entity = {}
        self.send_msg_to_devices(request)

    def click_on_text(self, text):
        request = Request()
        request.id = 3
        request.method = "ClickOnText"
        request.args = [text]
        self.send_msg_to_devices(request)

    def enter_text(self, code, text):
        request = Request()
        request.id = 4
        request.method = "EnterText"
        request.args = [code, text]
        self.send_msg_to_devices(request)

    def wait_for_text(self, text):
        request = Request()
        request.id = 5
        request.method = "WaitForText"
        request.args = [text]
        self.send_msg_to_devices(request)

    def click_on_view(self, code):
        request = Request()
        request.id = 6
        request.method = "ClickOnView"
        request.args = [code]
        self.send_msg_to_devices(request)

    def switch_to_tab(self, code, index):
        request = Request()
        request.id = 6
        request.method = "SwitchToTab"
        request.args = [code, index]
        self.send_msg_to_devices(request)

    def proxy_manager(self, devices, name, *args):
        for (id, device) in devices.items():
            self.target_devices.add(device)
        if name == 'startapp':
            self.start_app(args[0])
        elif name == 'waitfortext':
            self.wait_for_text(args[0])
        elif name == 'getview':
            self.get_view(args[0])
        elif name == 'entertext':
            self.enter_text(cache.entity.get("code"), args[1])
        elif name == 'clickontext':
            self.click_on_text(args[0])
        elif name == 'clickonview':
            self.click_on_view(cache.entity.get("code"))
        elif name == 'switchtotab':
            self.switch_to_tab(cache.entity.get("code"), args[1])
        elif name == 'finishapp':
            self.finish_app()
