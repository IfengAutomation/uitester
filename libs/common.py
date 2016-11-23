# @Time    : 2016/11/21 12:15
# @Author  : lixintong
from keywords import keyword, get_var, get_field, call
from primary import get_view

tab_view_pos = {
    '首页': 0,
    '直播': 1,
    '订阅': 2,
    '我的': 3
}
page_name_ui_controller = {'点播底页': 'com.ifeng.newvideo.videoplayer.activity.ActivityVideoPlayerDetail',
                           '自媒体': 'com.ifeng.newvideo.ui.subscribe.WeMediaHomePageActivity',
                           '登录': 'com.ifeng.newvideo.login.activity.LoginMainActivity'
                           }


@keyword("check_current_page")
def check_current_page(page_name):
    """
    功能：判断当前是否为某页
    :param player_type:"自媒体" 、"登录"、"点播底页"
    :return:
    """
    solo = get_var("solo")
    expect_page = page_name_ui_controller[page_name]
    # solo.sleep(3000)
    current_activity = solo.get_current_activity()
    result = expect_page == current_activity.class_name
    assert result, "非{}页面".format(page_name)


@keyword("get_current_progress")
def get_current_progress(index=0):
    """
    功能：获取s播放器播放进度
    :param index:"0"
    :return:
    """
    seekbar_id = "com.ifeng.newvideo:id/control_seekBar"
    solo = get_var("solo")
    # solo.sleep(3000)
    view = solo.get_view(res_id=seekbar_id, index=index)
    mSeekBarView = get_field(view, "mSeekBarView")
    progress = call(mSeekBarView, "getProgress")
    return progress


@keyword("check_video_state")
def check_video_state(state):
    """
    功能 检查播放器状态
    :param state: "playing"、"pause"
    :return:
    """
    solo = get_var("solo")
    video_skin = solo.get_view("com.ifeng.newvideo:id/video_skin")
    description = call(video_skin, "getContentDescription")
    assert description == state, "视频状态非{}".format(state)


@keyword("switch_tab")
def switch_tab(tab_name):
    """
    切换栏目
    :param tab_name:"首页"、"直播"、""订阅、"我的"
    :return:
    """
    solo = get_var("solo")
    tab_view = get_view("android:id/tabs")
    view = call(tab_view, "getChildTabViewAt", tab_view_pos[tab_name])
    solo.click_on_view(view)


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
    solo = get_var("solo")
    context = call(edit_text_view, "getContext")
    input_manager = call(context, "getSystemService", "input_method")
    return call(input_manager, "isActive")


@keyword("assert_string_empty")
def assert_string_empty(text):
    if text:
        raise AssertionError('% not empty' % text)


@keyword("assert_text_exist")
def assert_exist_text(text):
    solo = get_var("solo")
    exist = solo.wait_for_text(text)
    if not exist:
        raise AssertionError('%s is not exist' % text)


@keyword("assert_text_not_exist")
def assert_exist_text(text):
    solo = get_var("solo")
    exist = solo.wait_for_text(text)
    if exist:
        raise AssertionError('%s is exist' % text)


@keyword("finish_app")
def finish_app():
    """
    finish app
    :return:
    """
    solo = get_var("solo")
    solo.finish_opened_activities()

