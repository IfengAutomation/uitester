# @Time    : 2016/11/18 16:32
from keywords import keyword, call, get_solo, get_ui_device
from remote_classes import AdapterView, View

SCREEN_ORIENTATION_LANDSCAPE = 0
SCREEN_ORIENTATION_PORTRAIT = 1


@keyword("click_id")
def click_id(view_id, index=0):
    """
    click a view matching the specified resource view_id
    :param view_id:id the id of the {@link View}
    :param index:the index of the {@link View}. {@code 0} if only one is available
    :return:
    """
    view = get_view(view_id, index)
    click_view(view)


@keyword("click_text")
def click_text(text):
    """
    Clicks a View or WebElement displaying the specified text. Will automatically scroll when needed.
    :param text:the text to click. The parameter will be interpreted as a regular expression
    :return:
    """
    get_solo().click_on_text(text)


@keyword("click_view")
def click_view(view):
    """
    Clicks the specified View.
    :param view:the {@link View} to click
    :return:
    """
    get_solo().click_on_view(view)


@keyword("get_view")
def get_view(view_id, index=0):
    """
    Returns a View matching the specified resource id and index.
    :param view_id:the view_id of the {@link View}
    :param index:the index of the {@link View}. {@code 0} if only one is available
    :return:a {@link View} matching the specified id and index
    """
    return get_solo().get_view(res_id=view_id, index=index)


@keyword("get_view_text")
def get_view_text(view_id, index=0):
    """
    Returns a TextView matching the specified index.
    :param view_id:the view_id of the {@link View}
    :param index:the index of the {@link TextView}. {@code 0} if only one is available
    :return:a {@link TextView} matching the specified index
    """
    view = get_solo().get_view(res_id=view_id, index=index)
    return call(view, "getText")


@keyword("sleep")
def sleep(milliseconds):
    """
    Robotium will sleep for the specified time.
    :param milliseconds:the time in milliseconds that Robotium should sleep
    :return:
    """
    get_solo().sleep(milliseconds)


@keyword("wait_for_view")
def wait_for_view(class_name):
    """
     Waits for a View matching the specified class. Default timeout is 20 seconds.
    :param class_name:the {@link View} class to wait for
    :return:{@code true} if the {@link View} is displayed and {@code false} if it is not displayed before the timeout
    """
    return get_solo().wait_for_view(class_name)


@keyword("get_text_view_line_count")
def get_text_view_line_count(view):
    """
    get textView line count
    :param view:the type of textView
    :return:
    """
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


@keyword("get_view_from_parent")
def get_view_from_parent(parent, res_id):
    """
    get View from parent view's children by view id string
    :param parent:
    :param res_id:
    :param index:
    :return:
    """
    return get_solo().get_view_from_parent(parent, res_id)


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
     :return: True if found the text
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
    """
    get textView soft input state
    :param edit_text_view: type of textView
    :return: false or true;false means soft input is not active  ;true means soft input is active
    """
    context = call(edit_text_view, "getContext")
    input_manager = call(context, "getSystemService", "input_method")
    return call(input_manager, "isActive")


@keyword("assert_string_empty")
def assert_string_empty(text):
    """
    assert text is empty
    :param text:
    :return:
    """
    if text:
        raise AssertionError('% not empty' % text)


@keyword("assert_text_exist")
def assert_text_exist(text):
    """
    assert text is existed
    :param text:
    :return:
    """
    solo = get_solo()
    exist = solo.wait_for_text(text)
    if not exist:
        raise AssertionError('%s is not exist' % text)


@keyword("assert_text_not_exist")
def assert_text_not_exist(text):
    """
    assert text is not existed
    :param text:
    :return:
    """
    solo = get_solo()
    exist = solo.wait_for_text(text)
    if exist:
        raise AssertionError('%s is exist' % text)


@keyword("assert_view_is_show")
def assert_view_is_show(view):
    """
    assert view is shown
    :param view:
    :return:
    """
    is_shown = call(view, "isShown")
    if not is_shown:
        raise AssertionError('%s is not show' % view)


@keyword("assert_view_not_show")
def assert_view_not_show(view):
    """
    assert view is hidden
    :param view:
    :return:
    """
    is_shown = call(view, "isShown")
    if is_shown:
        raise AssertionError('%s is show' % view)


@keyword("set_screen_landscape")
def set_screen_landscape():
    """
    set screen landscape
    :return:
    """
    solo = get_solo()
    call(solo, "setActivityOrientation", SCREEN_ORIENTATION_LANDSCAPE)


@keyword("set_screen_portrait")
def set_screen_portrait():
    """
    set screen portrait
    :return:
    """
    solo = get_solo()
    current_activity = solo.get_current_activity()
    call(current_activity, "setRequestedOrientation", SCREEN_ORIENTATION_PORTRAIT)


@keyword("click_long_on_view")
def click_long_on_view(view):
    """
    Long clicks the specified View.
    :param view:the {@link View} to long click
    :return:
    """
    get_solo().click_long_on_view(view)


@keyword("go_back")
def go_back():
    """
    Simulates pressing the hardware back key.
    :return:
    """
    get_solo().go_back()


@keyword("set_edit_text")
def set_edit_text(edit_text_view, text):
    """
    Enters text in the specified EditText.
    :param edit_text_view: the {@link EditText} to enter text in
    :param text: the text to enter in the {@link EditText} field
    """
    get_solo().enter_text(edit_text_view, text)


@keyword("clear_edit_text")
def clear_edit_text(edit_text_view):
    """
    Clears the value of an EditText.
    :param edit_text_view: the {@link EditText} to clear
    """
    get_solo().clear_edit_text(edit_text_view)


@keyword("click_on_screen")
def click_on_screen(x, y):
    """
    Clicks the specified coordinates.
    :param x: the x coordinate
    :param y: the y coordinate
    """
    get_solo().click_on_screen(x, y)


@keyword("get_web_url")
def get_web_url():
    """
    Returns the current web page URL.
    :return:the current web page URL
    """
    return call(get_solo(), "getWebUrl")


@keyword("assert_contain_text")
def assert_contain_text(src_text, desc_text):
    """
    assert src_text contain desc_text
    :param src_text:
    :param desc_text:
    :return:
    """
    is_contain_text = desc_text in src_text
    if not is_contain_text:
        raise AssertionError('% not contain %' % (src_text, desc_text))


@keyword("scroll_view_to_left")
def scroll_view_to_left(view):
    """
    scroll view to left
    :param view:
    :return:
    """
    get_solo().scroll_view_to_left(view)


@keyword("scroll_view_to_right")
def scroll_view_to_right(view):
    """
    scroll view to right
    :param view:
    :return:
    """
    get_solo().scroll_view_to_right(view)


@keyword("assert_view_is_focused")
def assert_view_is_focused(view):
    """
    验证指定view的isFocused属性是否为True
    :param view:
    :return:
    """
    view = View.from_object(view)
    is_focused = view.is_focused()

    if not is_focused:
        AssertionError('%s is not focused' % view)


@keyword("assert_view_is_enabled")
def assert_view_is_enabled(view):
    """
    验证指定view的isEnabled属性是否为True
    :param view:
    :return:
    """
    view = View.from_object(view)
    is_enabled = view.is_enabled()

    if not is_enabled:
        AssertionError('%s is not enabled' % view)


@keyword("assert_view_is_not_enabled")
def assert_view_is_not_enabled(view):
    """
    验证指定view的isEnabled属性是否为False
    :param view:
    :return:
    """
    view = View.from_object(view)
    is_enabled = view.is_enabled()

    if is_enabled:
        AssertionError('%s is enabled' % view)


@keyword("get_child_view")
def get_child_view(parent_view, index=1):
    """
    通过parent_view 获取 index 位置的view
    :param parent_view: 父级view,view继承ViewGroup
    :param index:第index位置
    :return:
    """
    return call(parent_view, "getChildAt", index - 1)

@keyword("perform_click_view")
def perform_click_view(view):
    get_solo().perform_click_on_view(view)



