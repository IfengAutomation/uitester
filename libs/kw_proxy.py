
class View:
    id = None
    text = None
    clazz = None


class KWProxy:

    def get_view(self, view_id):
        """
        get view by id
        :param view_id:
        :return View instance
        """
        pass

    def start_app(self, package_name):
        """
        start app by package name
        :param package_name:
        :return: None
        """
        pass

    def finish_app(self):
        """

        :return:
        """
        pass

    def click_on_text(self, text):
        """
        click on text
        :param text:
        :return:
        """
        pass

    def enter_text(self, view, text):
        """
        Enter text to view
        :param view:
        :param text:
        :return:
        """
        pass

    def wait_for_text(self, text):
        """
        Wait for text
        :param text:
        :return:
        """
        pass

    def click_on_view(self, view_id):
        """
        Click on view by id
        :param view_id:
        :return:
        """
        pass

    def click(self, view):
        """
        Click on view
        :param view:
        :return:
        """
        pass
