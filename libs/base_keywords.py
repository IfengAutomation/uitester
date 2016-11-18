# @Time    : 2016/11/18 16:32
from keywords import get_var, keyword, call

solo = get_var("solo")


@keyword("click_id")
def click_id(view_id):
    view = get_view(view_id)
    click_view(view)


@keyword("click_text")
def click_text(text):
    solo.click_on_text(text)


@keyword("click_view")
def click_view(view):
    solo.click_on_view(view)


@keyword("get_view")
def get_view(view_id):
    return solo.get_view(res_id=view_id)


@keyword("get_view_text")
def get_text(view_id, index="0"):
    view = solo.get_view(res_id=view_id, index=int(index))
    return call(view, "getText")


@keyword("sleep")
def sleep(milliseconds):
    solo.sleep(int(milliseconds))


