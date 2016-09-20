import logging
from uitester.test_manager import context

logger = logging.getLogger('Tester')


class View:
    pass


def get_view(view_id):
    """
    Get view by android id
    e.g.
    get_view android:id/list as v

    :param view_id:
    :return:view
    """
    response = context.agent.call('GetView', view_id)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    view_dict = response.args[0]
    v = View()
    v.__dict__ = view_dict
    return v


def start_app(context, package_name):
    """
    Start app by package name
    :param package_name:
    :return:
    """
    response = context.agent.call('StartMainActivity', package_name)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def finish_app(context):
    """
    Finish all activity
    :return:
    """
    response = context.agent.call('FinishActivity')
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def click_on_text(context, text):
    """
    Click on text

    :param text:
    :return:
    """
    response = context.agent.call('ClickOnText', text)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def enter_text(context, view, text):
    """
    Enter text to a editor view

    :param view:
    :param text:
    :return:
    """
    response = context.agent.call('EnterText', view.hash, text)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def wait_for_text(context, text):
    """
    Wait text
    :param text:
    :return:
    """
    response = context.agent.call('WaitForText', text)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def click_on_view(context, view):
    """
    Click on view
    :param view:
    :return:
    """
    response = context.agent.call('ClickOnView', view.hash)
    if response.name == 'error':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]

