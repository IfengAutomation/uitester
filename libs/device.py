from keywords import var_cache, keyword


@keyword('get_list_view')
def get_view(view_id):
    """

    :param view_id:
    :return:
    """
    return var_cache['proxy'].get_view(view_id)


@keyword('click_on_text')
def click_on_text(text):
    """

    :param text:
    :return:
    """
    return var_cache['proxy'].click_on_text(text)


@keyword('click_on_view')
def click_on_view(view):
    """

    :param view:
    :return:
    """
    return var_cache['proxy'].click_on_view(view)


@keyword('launch_app')
def launch_app(package_name):
    """

    :param package_name:
    :return:
    """
    return var_cache['proxy'].launch_app(package_name)


@keyword('wait_for_text')
def wait_for_text(text):
    """
    wait for text
    :param text:
    :return:
    """
    return var_cache['proxy'].wait_for_text(text)


@keyword('get_list_item')
def get_list_item(view, index):
    """
    get item from listView by index
    :param view:
    :param index:
    :return:
    """
    return var_cache['proxy'].get_list_item(view, index)


@keyword('load_more')
def load_more(view):
    """
    load more
    :param view:
    :return:
    """
    return var_cache['proxy'].load_more(view)


@keyword('refresh_content')
def refresh_content(view):
    """
    refresh content for listView
    :param view:
    :return:
    """
    return var_cache['proxy'].refresh_content(view)


@keyword('find_view_by_id')
def find_view_by_id(parent_view, view_id):
    """
    get view by id
    :param parent_view:
    :param view_id:
    :return:
    """
    return var_cache['proxy'].find_view_by_id(parent_view, view_id)


@keyword('switch_to_tab')
def switch_to_tab(view, index):
    """
    switch to tab
    :param view:
    :param index:
    :return:
    """
    return var_cache['proxy'].switch_to_tab(view, index)


@keyword('enter_text')
def enter_text(view, text):
    """
    enter text into TextView
    :param view:
    :param text:
    :return:
    """
    return var_cache['proxy'].enter_text(view, text)


@keyword('get_list_count')
def get_list_count(view):
    """
    get listView's count
    :param view:
    :return:
    """
    return var_cache['proxy'].get_list_count(view)
