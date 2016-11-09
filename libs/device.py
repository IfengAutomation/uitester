kw_func = {}

var_cache = {}


def keyword(name):
    def _register(func):
        kw_func[name] = func
        return func
    return _register


class View:

    def __init__(self):
        self.id = ''
        self.clazz = ''
        self.text = ''
        self.hash = 0


@keyword('getView')
def get_view(view_id):
    """

    :param view_id:
    :return:
    """
    return var_cache['proxy'].get_view(view_id)


@keyword('clickOnText')
def click_on_text(text):
    """

    :param text:
    :return:
    """
    return var_cache['proxy'].click_on_text(text)


@keyword('clickOnView')
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


@keyword('waitForText')
def wait_for_text(text):
    """
    wait for text
    :param text:
    :return:
    """
    return var_cache['proxy'].wait_for_text(text)


@keyword('getListItem')
def get_list_item(view, index):
    """
    get item from listView by index
    :param view:
    :param index:
    :return:
    """
    return var_cache['proxy'].get_list_item(view, index)


@keyword('loadMore')
def load_more(view):
    """
    load more
    :param view:
    :return:
    """
    return var_cache['proxy'].load_more(view)


@keyword('refreshContent')
def refresh_content(view):
    """
    refresh content for listView
    :param view:
    :return:
    """
    return var_cache['proxy'].refresh_content(view)


@keyword('getTitle')
def get_title(view, title_id):
    """
    get listView Item's title
    :param view: item's view
    :param title_id:title's id
    :return:
    """
    return var_cache['proxy'].get_title(view, title_id)
