# @Time    : 2016/11/16 15:48
# @Author  : lixintong
from keywords import keyword, get_var, call
from player import check_view_exist, click_view, get_view_by_id, sleep

video_detail_title_id = "com.ifeng.newvideo:id/video_detail_title"
video_detail_open_id = "com.ifeng.newvideo:id/video_detail_open"
video_detail_desc_id = "com.ifeng.newvideo:id/video_detail_desc"
video_play_count_id = "com.ifeng.newvideo:id/video_detail_play_count"
video_user_name_id = "com.ifeng.newvideo:id/video_detail_user_name"
video_user_icon_id = "com.ifeng.newvideo:id/video_detail_user_icon_mask"
comment_input_id = "com.ifeng.newvideo:id/bottom_comment_input"
send_comment_edit_id = "com.ifeng.newvideo:id/send_comment_edit"
video_ad_container_id = "com.ifeng.newvideo:id/video_detail_ad_container"
video_recommend_id = "com.ifeng.newvideo:id/view_parent"
video_recommend_container_id = "com.ifeng.newvideo:id/video_detail_recommend_top_container"
video_recommend_show_more_id = "com.ifeng.newvideo:id/video_detail_recommend_show_more"


@keyword("click_video_detail_desc")
def click_video_detail_desc():
    solo = get_var("solo")
    video_detail_open_view = solo.get_view(video_detail_open_id)
    solo.click_on_view(video_detail_open_view)


@keyword("check_video_title_line")
def check_video_title_line(expect_line_count):
    expect_line_count = int(expect_line_count)
    solo = get_var("solo")
    video_title_view = solo.get_view(video_detail_title_id)
    result = call(video_title_view, "getLineCount")
    assert result <= expect_line_count, '点播视频标题行数错误'


@keyword("check_video_desc")
def check_video_desc(expect_desc=''):
    solo = get_var("solo")
    video_desc_view = solo.get_view(video_detail_desc_id)
    video_desc = call(video_desc_view, "getText")
    if expect_desc:
        assert video_desc == expect_desc, '点播视频简介错误'
    else:
        assert video_desc == '还没有简介', '点播视频简介错误'


@keyword("check_video_play_count")
def check_video_play_count(play_count):
    play_count = int(play_count)
    solo = get_var("solo")
    video_play_count_view = solo.get_view(video_play_count_id)
    play_message = call(video_play_count_view, "getText")
    if play_count < 10000:
        expect_play_count = play_count
        expect_play_message = "{}次播放".format(expect_play_count)
    elif play_count < 9999000:
        expect_play_count = '%.1f' % (play_count / 10000)
        expect_play_message = "{}万次播放".format(expect_play_count)
    else:
        expect_play_message = "999.9万次播放"
    assert expect_play_message == play_message, '点播视频播放次数不符合规则'


@keyword("click_video_user_name")
def click_video_user_name():
    solo = get_var("solo")
    view = solo.get_view(video_user_name_id)
    solo.click_on_view(view)


@keyword("click_video_user_icon")
def click_video_user_name():
    solo = get_var("solo")
    view = solo.get_view(video_user_icon_id)
    solo.click_on_view(view)


@keyword("check_video_comment_exist")
def check_video_comment_exist(expect_result, is_zero_count):
    if is_zero_count == "false" or is_zero_count == "False":
        is_zero_count = False
    elif is_zero_count == "true" or is_zero_count == "True":
        is_zero_count = True
    else:
        raise ValueError('state 值错误')
    if is_zero_count:
        check_view_exist(send_comment_edit_id, expect_result)
    else:
        check_view_exist(comment_input_id, expect_result)


@keyword("click_video_player_view")
def click_video_player_view():
    click_view("com.ifeng.newvideo:id/video_skin")


@keyword("check_ad_container_exist")
def check_ad_container_exist(expect_result):
    check_view_exist(video_ad_container_id, expect_result)


@keyword("click_ad_container_view")
def click_ad_container_view():
    click_view(video_ad_container_id)


@keyword("get_video_recommends_count")
def get_video_recommends_count():
    recommend_top_container_view = get_view_by_id(video_recommend_container_id)
    sleep(3000)
    child_count = call(recommend_top_container_view, "getChildCount")
    return child_count


@keyword("check_video_show_more_exist")
def check_video_show_more_exist(expect_result):
    check_view_exist(video_recommend_show_more_id, expect_result)
