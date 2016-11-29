# @Time    : 2016/11/18 16:32
from keywords import keyword, call, get_solo, get_ui_device

SCREEN_ORIENTATION_LANDSCAPE = 0
SCREEN_ORIENTATION_PORTRAIT = 1


@keyword("click_id")
def click_id(view_id, index=0):
    view = get_view(view_id, index)
    click_view(view)


@keyword("click_text")
def click_text(text):
    get_solo().click_on_text(text)


@keyword("click_view")
def click_view(view):
    get_solo().click_on_view(view)


@keyword("get_view")
def get_view(view_id, index=0):
    return get_solo().get_view(res_id=view_id, index=index)


@keyword("get_view_text")
def get_text(view_id, index=0):
    view = get_solo().get_view(res_id=view_id, index=index)
    return call(view, "getText")


@keyword("sleep")
def sleep(milliseconds):
    get_solo().sleep(milliseconds)


@keyword("wait_for_view")
def wait_for_text(class_name):
    return get_solo().wait_for_view(class_name)


@keyword("get_text_view_line_count")
def get_text_view_line_count(view):
    return call(view, "getLineCount")


@keyword("finish_app")
def finish_app():
    """
    finish app
    :return:
    """
    get_solo().finish_opened_activities()


@keyword("scroll_to_right")
def scroll_to_right():
    """
    scroll to right
    :return:
    """
    get_solo().scroll_to_right()


@keyword("scroll_to_left")
def scroll_to_left():
    """
    scroll to left
    :return:
    """
    get_solo().scroll_to_left()


@keyword("get_text_from_parent")
def get_text_from_parent(view, text, index=0):
    """
    获取父级view下的指定文本,返回TextView

    用法示例:
    get_text_from_parent parent_view text 1
    
    注：index不输入时，默认为0
    :param view:
    :param text:
    :param index:
    :return:
    """
    return get_solo().get_text_from_parent(view, text, index)


@keyword("get_current_package_name")
def get_current_package_name():
    """
    获取当前应用的包名
    返回包名
    :return: str
    """
    return get_ui_device().get_current_package_name()


@keyword("press_home_button")
def press_home_button():
    """
    点击home键
    :return:
    """
    get_ui_device().press_home()


@keyword("scroll_down")
def scroll_down():
    """
    Scrolls down the screen.
    :return True if more scrolling can be performed and False if it is at the end of the screen
    """
    return get_solo().scroll_down()


@keyword("scroll_up")
def scroll_up():
    """
    Scrolls up the screen.
    :return: True if more scrolling can be performed and False if it is at the top of the screen
    """
    return get_solo().scroll_up()


@keyword("scroll_to_top")
def scroll_to_top():
    """
    Scrolls to the top of the screen.
    """
    return get_solo().scroll_to_top()


@keyword("scroll_to_bottom")
def scroll_to_bottom():
    """
    Scrolls to the bottom of the screen.
    """
    return get_solo().scroll_to_bottom()


@keyword("scroll_list_to_top")
def scroll_list_to_top(list_view):
    """
    Scrolls to the top of the specified AbsListView.
    :param list_view: the AbsListView to scroll
    :return: True if more scrolling can be performed
    """
    return get_solo().scroll_list_to_top(list_view)


@keyword("scroll_list_to_bottom")
def scroll_list_to_bottom(list_view):
    """
    Scrolls to the bottom of the specified AbsListView.
    :param list_view: the AbsListView to scroll
    :return: True if more scrolling can be performed
    """
    return get_solo().scroll_list_to_bottom(list_view)


@keyword("wait_text_in_list")
def wait_text_in_list(list_view, text):
    """
     Scroll list one screen by one. Not scroll line by line
     :param list_view:
     :param text:
     :return:
     """
    return get_solo().wait_text_in_list(list_view, text)


@keyword("get_displayed_views")
def get_displayed_views(id):
    """
    get views in window rect by view id str
    :param res_id:
    :return:
    """
    return get_solo().get_displayed_views(id)


@keyword("get_group_child_count")
def get_group_child_count(view_group):
    """
    功能：获取viewGroup child 数量
    :param view_group:
    :return:
    """
    return call(view_group, "getChildCount")


@keyword("get_soft_input_state")
def get_soft_input_state(edit_text_view):
    context = call(edit_text_view, "getContext")
    input_manager = call(context, "getSystemService", "input_method")
    return call(input_manager, "isActive")


@keyword("assert_string_empty")
def assert_string_empty(text):
    if text:
        raise AssertionError('% not empty' % text)


@keyword("assert_text_exist")
def assert_exist_text(text):
    solo = get_solo()
    exist = solo.wait_for_text(text)
    if not exist:
        raise AssertionError('%s is not exist' % text)


@keyword("assert_text_not_exist")
def assert_exist_text(text):
    solo = get_solo()
    exist = solo.wait_for_text(text)
    if exist:
        raise AssertionError('%s is exist' % text)


@keyword("assert_view_is_show")
def assert_view_hidden(view):
    is_shown = call(view, "isShown")
    if not is_shown:
        raise AssertionError('%s is not show' % view)


@keyword("assert_view_not_show")
def assert_view_not_show(view):
    is_shown = call(view, "isShown")
    if is_shown:
        raise AssertionError('%s is show' % view)


@keyword("set_screen_landscape")
def assert_exist_text():
    solo = get_solo()
    call(solo, "setActivityOrientation", SCREEN_ORIENTATION_LANDSCAPE)


@keyword("set_screen_portrait")
def assert_exist_text():
    solo = get_solo()
    current_activity = solo.get_current_activity()
    call(current_activity, "setRequestedOrientation", SCREEN_ORIENTATION_PORTRAIT)


@keyword("click_long_on_view")
def click_long_on_view(view):
    solo = get_solo()
    solo.click_long_on_view(view)


@keyword("go_back")
def click_long_on_view():
    solo = get_solo()
    solo.go_back()


@keyword("set_edit_text")
def set_edit_text(view, text):
    solo = get_solo()
    solo.enter_text(view, text)


@keyword("clear_edit_text")
def clear_edit_text(view):
    solo = get_solo()
    solo.clear_edit_text(view)
