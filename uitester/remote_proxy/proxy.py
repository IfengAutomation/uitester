from uitester.json_rpc.request import Request
import time


class CommonProxy:

    def __init__(self, context):
        self.context = context
        self.responses = []

        def response_callback(msg_type, msg=None):
            if msg_type == 'rpc_response' and msg is not None:
                self.responses.append(msg)
        self.context.register(response_callback)

    def _send_rpc_msg(self, request):
        self.context.publish('rpc_proxy', request)

    def _wait_for_response(self):
        while True:
            if len(self.responses) > 0:
                return self.responses.pop(0)
            time.sleep(0.5)

    def get_view(self, view_id):
        """
        Get view by android id
        e.g.
        get_view android:id/list as v

        :param view_id:
        :return:view
        """
        request = Request()
        request.method = "GetView"
        request.args = [view_id]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def start_app(self, package_name):
        """
        Start app by package name
        :param package_name:
        :return:
        """
        request = Request()
        request.method = "StartMainActivity"
        request.args = [package_name]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def finish_app(self):
        """
        Finish all activity
        :return:
        """
        request = Request()
        request.method = "FinishActivity"
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def click_on_text(self, text):
        """
        Click on text

        :param text:
        :return:
        """
        request = Request()
        request.method = "ClickOnText"
        request.args = [text]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def enter_text(self, view, text):
        """
        Enter text to a editor view

        :param view:
        :param text:
        :return:
        """
        request = Request()
        request.method = "EnterText"
        request.args = [view.hash, text]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def wait_for_text(self, text):
        """
        Wait text
        :param text:
        :return:
        """
        request = Request()
        request.method = "WaitForText"
        request.args = [text]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def click_on_view(self, view):
        """
        Click on view
        :param view:
        :return:
        """
        request = Request()
        request.method = "ClickOnView"
        request.args = [view.hash]
        self._send_rpc_msg(request)
        return self._wait_for_response()

    def switch_to_tab(self, view, index):
        """
        Switch to tab
        :param view:
        :param index:
        :return:
        """
        request = Request()
        request.method = "SwitchToTab"
        request.args = [view.hash, index]
        self._send_rpc_msg(request)
        return self._wait_for_response()


