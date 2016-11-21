# @Time    : 2016/11/21 12:15
# @Author  : lixintong
from base_keywords import get_view
from keywords import keyword, get_var, get_field, call, RemoteObject, call_static
from solo import InstrumentationRegistry

tab_view_pos = {
    '首页': 0,
    '直播': 1,
    '订阅': 2,
    '我的': 3
}
page_name_ui_controller = {'点播底页': 'com.ifeng.newvideo.videoplayer.activity.ActivityVideoPlayerDetail',
                           'topic_player': 'com.ifeng.newvideo.videoplayer.activity.ActivityTopicPlayer',
                           'live': 'com.ifeng.newvideo.ui.live.TVLiveActivity',
                           'pic_player': 'com.ifeng.newvideo.ui.UniversalChannelFragment',
                           'local_player': 'com.ifeng.newvideo.ui.live.VRLiveActivity',
                           'vr_live': 'com.ifeng.newvideo.videoplayer.activity.ActivityCacheVideoPlayer',
                           '自媒体': 'com.ifeng.newvideo.ui.subscribe.WeMediaHomePageActivity',
                           '登录': 'com.ifeng.newvideo.login.activity.LoginMainActivity'
                           }


@keyword("check_current_page")
def check_current_page(page_name):
    """
    功能：判断当前是否为某页
    :param player_type:自媒体 、 点播底页 、 topic_player or live 、pic_player 、 local_player
    :param expect_result: true or false
    :return:
    """
    solo = get_var("solo")
    expect_page = page_name_ui_controller[page_name]
    solo.sleep(3000)
    current_activity = solo.get_current_activity()  # todo 大图播放页
    result = expect_page == current_activity.class_name
    assert result, "非{}页面".format(page_name)


@keyword("get_current_progress")
def get_current_progress(index="0"):
    """
    背景：在视频播放底页或大图频道
    功能：获取当前播放进度
    :param player_type:
    :param index:
    :return:
    """
    seekbar_id = "com.ifeng.newvideo:id/control_seekBar"
    solo = get_var("solo")
    solo.sleep(3000)
    view = solo.get_view(res_id=seekbar_id, index=int(index))
    mSeekBarView = get_field(view, "mSeekBarView")
    progress = call(mSeekBarView, "getProgress")
    return progress


@keyword("check_video_state")
def check_video_state(state):
    solo = get_var("solo")
    solo.sleep(3000)
    video_skin = solo.get_view("com.ifeng.newvideo:id/video_skin")
    description = call(video_skin, "getContentDescription")
    assert description == state, "视频状态非{}".format(state)


@keyword("switch_tab")
def switch_tab(tab_name):
    solo = get_var("solo")
    tab_view = get_view("android:id/tabs")
    view = call(tab_view, "getChildTabViewAt", tab_view_pos[tab_name])
    solo.click_on_view(view)


# class PlayerCommon:
#     class_name = "com.ifeng.at.testagent.driver.methodImpl.PlayerCommon"
#     remote_obj = RemoteObject.from_class_name(class_name)
#
#     @classmethod
#     def hasKeyboard(cls, solo):
#         return call_static(cls.remote_obj, "hasKeyboard", solo)


@keyword("check_keyboard")
def check_keyboard():
    solo = get_var("solo")
    solo.sleep(3000)#todo 修改
    # getWindow().peekDecorView()
    # solfInputState = PlayerCommon.hasKeyboard(solo)
    # assert solfInputState != None, "键盘未显示"
    # # getCurrentActivity().getWindow().peekDecorView()
    # input_method_manager = InstrumentationRegistry.get_instrumentation().get_target_context().get_system_service()
    # view = get_view("com.ifeng.newvideo:id/send_comment_edit")
    # keyboard_state = call(input_method_manager, "isActive", view)
    # assert keyboard_state, "键盘未显示"
