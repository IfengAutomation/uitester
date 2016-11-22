# @Time    : 2016/11/18 16:32
from keywords import get_var, keyword, call


@keyword("click_id")
def click_id(view_id, index=0):
    solo = get_var("solo")
    solo.sleep(3000)
    view = get_view(view_id, index)
    click_view(view)


@keyword("click_text")
def click_text(text):
    solo = get_var("solo")
    solo.click_on_text(text)


@keyword("click_view")
def click_view(view):
    solo = get_var("solo")
    solo.click_on_view(view)


@keyword("get_view")
def get_view(view_id, index=0):
    solo = get_var("solo")
    return solo.get_view(res_id=view_id, index=index)


@keyword("get_view_text")
def get_text(view_id, index=0):
    solo = get_var("solo")
    view = solo.get_view(res_id=view_id, index=index)
    return call(view, "getText")


@keyword("sleep")
def sleep(milliseconds):
    solo = get_var("solo")
    solo.sleep(milliseconds)