# @Time    : 2016/11/11 11:01
# @Author  : lixintong
from keywords import keyword, var_cache, get_var, call_static, RemoteObject, call, get_field

player_page = {'video_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityVideoPlayerDetail',
               'topic_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityTopicPlayer',
               'live': 'com.ifeng.newvideo.ui.live.TVLiveActivity',
               'pic_player': 'com.ifeng.newvideo.ui.UniversalChannelFragment',
               'local_player': 'com.ifeng.newvideo.ui.live.VRLiveActivity',
               'vr_live': 'com.ifeng.newvideo.videoplayer.activity.ActivityCacheVideoPlayer'
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
    view = solo.get_view(res_id=id, index=int(index))
    solo.click_on_view(view)


@keyword("check_current_page")
def check_current_page(player_type, expect_result):
    """
    背景：在某视频播放底页
    功能：判断当前是否为某播放视频底页
    :param player_type:video_player or topic_player or live or pic_player or local_player
    :param expect_result: true or false
    :return:
    """
    solo = get_var("solo")
    expect_page = player_page[player_type]
    solo.sleep(3000)
    current_activity = solo.get_current_activity()
    result = expect_page == current_activity.class_name
    if expect_result == "false" or expect_result == "False":
        expect_result = False
    elif expect_result == "true" or expect_result == "True":
        expect_result = True
    else:
        raise ValueError('expect_result 值错误')
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


@keyword("check_progress")
def check_progress(arg1, agr2, expect_result):
    """
    功能：比较进度值
    :param arg1:
    :param agr2:
    :param expect_result:
    :return:
    """
    arg1 = int(arg1)
    arg2 = int(agr2)
    if arg1 > arg2:
        result = '>'
    elif arg1 < agr2:
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
    video_state = PlayerCommon.is_play(solo, player_page[player])
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
