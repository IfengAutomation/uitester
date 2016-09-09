from uitester import cache
from uitester.json_rpc.request import Request


class CommonProxy:
    target_devices = set([])

    def _send_msg_to_devices(self, request):
        # TODO
        pass

    def get_view(self, view_id):
        request = Request()
        request.id = 0
        request.method = "GetView"
        request.args = [view_id]
        self._send_msg_to_devices(request)

    def start_app(self, package_name):
        request = Request()
        request.id = 1
        request.method = "StartMainActivity"
        request.args = [package_name]
        self._send_msg_to_devices(request)

    def finish_app(self):
        request = Request()
        request.id = 2
        request.method = "FinishActivity"
        cache.entity = {}
        self._send_msg_to_devices(request)

    def click_on_text(self, text):
        request = Request()
        request.id = 3
        request.method = "ClickOnText"
        request.args = [text]
        self._send_msg_to_devices(request)

    def enter_text(self, view, text):
        request = Request()
        request.id = 4
        request.method = "EnterText"
        request.args = [view.hash, text]
        self._send_msg_to_devices(request)

    def wait_for_text(self, text):
        request = Request()
        request.id = 5
        request.method = "WaitForText"
        request.args = [text]
        self._send_msg_to_devices(request)

    def click_on_view(self, view):
        request = Request()
        request.id = 6
        request.method = "ClickOnView"
        request.args = [view.hash]
        self._send_msg_to_devices(request)

    def switch_to_tab(self, view, index):
        request = Request()
        request.id = 6
        request.method = "SwitchToTab"
        request.args = [view.hash, index]
        self._send_msg_to_devices(request)

