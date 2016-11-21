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
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    view_dict = response.args[0]
    v = View()
    v.__dict__ = view_dict
    return v


def launch_app(package_name):
    """
    Start app by package name
    :param package_name:
    :return:
    """
    response = context.agent.call('LaunchApp', package_name)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def finish_app():
    """
    Finish all activity
    :return:
    """
    response = context.agent.call('FinishActivity')
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def click_on_text(text):
    """
    Click on text

    :param text:
    :return:
    """
    response = context.agent.call('ClickOnText', text)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def enter_text(view, text):
    """
    Enter text to a editor view

    :param view:
    :param text:
    :return:
    """
    response = context.agent.call('EnterText', view.hash, text)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def wait_for_text(text):
    """
    Wait text
    :param text:
    :return:
    """
    response = context.agent.call('WaitForText', text)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def click_on_view(view):
    """
    Click on view
    :param view:
    :return:
    """
    response = context.agent.call('ClickOnView', view.hash)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    return response.args[0]


def get_list_item(view, index):
    """
    Get item from listView by index
    :param view:
    :param index:
    :return:
    """
    response = context.agent.call('GetListItem', view.hash, index)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    view_dict = response.args[0]
    v = View()
    v.__dict__ = view_dict
    return v


def load_more(view):
    """
    load more
    :param view:
    :return:
    """
    response = context.agent.call('LoadMore', view.hash)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    return response.args[0]


def refresh_content(view):
    """
    refresh content
    :param view:
    :return:
    """
    response = context.agent.call('RefreshContent', view.hash)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    return response.args[0]


def find_view_by_id(parent_view, view_id):
    """
    find view by id
    :param parent_view: parentView
    :param view_id:
    :return:
    """
    response = context.agent.call('FindViewById', parent_view.hash, view_id)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None

    view_dict = response.args[0]
    v = View()
    v.__dict__ = view_dict
    return v


def switch_to_tab(view, index):
    """
    switch to tab
    :param view:
    :param index:
    :return:
    """
    response = context.agent.call('SwitchToTab', view.hash, index)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    return response.args[0]


def get_list_count(view):
    """
    get listView's count
    :param view:
    :return:
    """
    response = context.agent.call('GetListData', view.hash)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    view_dict = response.args[0]
    v = View()
    v.__dict__ = view_dict
    return v



def change_video_state(player_name, state):
    """
    :param player_name: video_player or topic_player or live or vr_live or pic_player or local_player
    :param state: play or pause
    :return:
    """
    response = context.agent.call('ChangeVideoState', player_name, state)
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    return response.args[0]


def deal_response(response):
    if response.name == 'Fail':
        raise ValueError(*response.args)
    if len(response.args) == 0:
        return None
    return response.args[0]
