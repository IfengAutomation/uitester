# @Time    : 2016/11/11 11:01
# @Author  : lixintong
from keywords import keyword, var_cache, get_var, call_static, RemoteObject, call, get_field

page = {'video_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityVideoPlayerDetail',
        'topic_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityTopicPlayer',
        'live': 'com.ifeng.newvideo.ui.live.TVLiveActivity',
        'pic_player': 'com.ifeng.newvideo.ui.UniversalChannelFragment',
        'local_player': 'com.ifeng.newvideo.ui.live.VRLiveActivity',
        'vr_live': 'com.ifeng.newvideo.videoplayer.activity.ActivityCacheVideoPlayer',
        'we_media': 'com.ifeng.newvideo.ui.subscribe.WeMediaHomePageActivity',
        'login': 'com.ifeng.newvideo.login.activity.LoginMainActivity'
        }

player_title_id = {
    'video_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityVideoPlayerDetail',
    'topic_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityTopicPlayer',
    'live': 'com.ifeng.newvideo.ui.live.TVLiveActivity',

    'pic_player': 'com.ifeng.newvideo:id/tv_channel_big_pic_title',

    'local_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityCacheVideoPlayer',
    'vr_live': 'com.ifeng.newvideo.ui.live.VRLiveActivity'

}

player_seekbar_id = {
    'video_player': 'com.ifeng.newvideo:id/control_seekBar',
    'pic_player': 'com.ifeng.newvideo:id/control_seekBar'
}
title_back = {
    'video_player': 'com.ifeng.newvideo:id/video_title_back'
}

tab_view_pos = {
    '首页': 0,
    '直播': 1,
    '订阅': 2,
    '我的': 3
}
toast_text_id = "com.ifeng.newvideo:id/toast_text"
tabs_id = "android:id/tabs"


@keyword("click_interactive_bar")
def click_interactive_bar(player_type, index=0):
    """
    背景：在视频列表页
    功能：点击某个视频标题，进入视频播放底页
    :param player_type:video_player or topic_player or live or pic_player or local_player
    :param index:
    :return:
    """
    id = player_title_id.get(player_type)
    solo = get_var("solo")
    sleep(3000)
    view = solo.get_view(res_id=id, index=int(index))
    solo.click_on_view(view)
    # click_view(player_title_id[player_type])


@keyword("check_current_page")
def check_current_page(player_type, expect_result):
    """
    功能：判断当前是否为某页
    :param player_type:we_media or video_player or topic_player or live or pic_player or local_player
    :param expect_result: true or false
    :return:
    """
    solo = get_var("solo")
    expect_page = page[player_type]
    solo.sleep(3000)
    current_activity = solo.get_current_activity()
    result = expect_page == current_activity.class_name
    expect_result = change_to_bool(expect_result)
    assert result == bool(expect_result), "非{}页面".format(player_type)


@keyword('change_video_state')
def change_video_state(player_name, state):
    """
    背景：在视频播放底页
    功能：改变视频播放状态
    :param player_name: video_player or topic_player or live or pic_player or local_player
    :param state: play or pause
    :return:
    """
    return var_cache['proxy'].change_video_state(player_name, state)


@keyword("get_current_progress")
def get_current_progress(player_type, index=0):
    """
    背景：在视频播放底页或大图频道
    功能：获取当前播放进度
    :param player_type:
    :param index:
    :return:
    """
    seekbar_id = player_seekbar_id.get(player_type)
    solo = get_var("solo")
    view = solo.get_view(res_id=seekbar_id, index=int(index))
    if view is None:
        video_skin = solo.get_view("com.ifeng.newvideo:id/video_skin")
        solo.click_on_view(video_skin)
    view = solo.get_view(res_id=seekbar_id, index=int(index))
    mSeekBarView = get_field(view, "mSeekBarView")
    progress = call(mSeekBarView, "getProgress")
    return progress


@keyword("check_relation")
def check_relation(arg1, agr2, expect_result):
    """
    功能：比较进度值
    :param arg1:
    :param agr2:
    :param expect_result:
    :return:
    """
    # arg1 = int(arg1)
    # int_arg2 = int(agr2)
    if int(arg1) > int(agr2):
        result = '>'
    elif int(arg1) < int(agr2):
        result = '<'
    else:
        result = '='
    assert result in expect_result, "预期关系错误"


class PlayerCommon:
    class_name = "com.ifeng.at.testagent.driver.methodImpl.PlayerCommon"
    remote_obj = RemoteObject.from_class_name(class_name)

    @classmethod
    def is_play(cls, solo, player_name):
        return call_static(cls.remote_obj, "isPlay", solo, player_name)


@keyword("is_play")
def is_play(player, state):
    """
    判断视频播放状态
    :param player:
    :param state:
    :return:
    """
    solo = get_var("solo")
    solo.sleep(3000)
    video_state = PlayerCommon.is_play(solo, page[player])
    if state == "false" or state == "False":
        expect_state = False
    elif state == "true" or state == "True":
        expect_state = True
    else:
        raise ValueError('state 值错误')
    assert video_state == expect_state, "预期状态错误"


@keyword("click_go_back")
def click_go_back(player_type):
    solo = get_var("solo")
    title_back_view = solo.get_view(title_back[player_type])
    solo.click_on_view(title_back_view)


@keyword("check_view_exist")
def check_view_exist(view_id, expect_result):
    solo = get_var("solo")
    view = solo.get_view(view_id)
    visibility = call(view, "getVisibility")
    if visibility == 0:
        result_state = True
    else:
        result_state = False
    if expect_result == 'True' or expect_result == 'true':
        expect_result = True
    elif expect_result == 'False' or expect_result == 'false':
        expect_result = False
    else:
        raise ValueError('expect_result 值错误')
    assert expect_result == result_state, "view exist 期待值与实际值不符"


@keyword("click_view")
def click_view(view_id):
    solo = get_var("solo")
    view = solo.get_view(view_id)
    solo.click_on_view(view)


def change_to_bool(var):
    if var == 'False' or var == 'false':
        return False
    elif var == 'True' or var == 'true':
        return True
    else:
        raise ValueError("参数错误")


def get_view_by_id(view_id):
    solo = get_var("solo")
    return solo.get_view(view_id)


def get_text_by_id(view_id):
    solo = get_var("solo")
    view = solo.get_view(view_id)
    return call(view, "getText")


def sleep(milliseconds):
    solo = get_var("solo")
    solo.sleep(milliseconds)


@keyword("check_toast_text")
def check_toast_text(text, expect_result):
    solo = get_var("solo")
    solo.sleep(1000)
    view_text = get_text_by_id(toast_text_id)
    expect_result = change_to_bool(expect_result)
    result = view_text == text
    assert result == expect_result, "toast text 实际与期望值不符"


@keyword("click_main_tab")
def click_main_tab(view_desc):
    solo = get_var("solo")
    tab_view = get_view_by_id(tabs_id)
    view = call(tab_view, "getChildTabViewAt", tab_view_pos[view_desc])
    solo.click_on_view(view)
