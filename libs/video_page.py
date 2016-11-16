# @Time    : 2016/11/16 15:48
# @Author  : lixintong
from keywords import keyword, get_var, call

video_detail_title_id = "com.ifeng.newvideo:id/video_detail_title"
video_detail_open_id = "com.ifeng.newvideo:id/video_detail_open"
video_detail_desc_id = "com.ifeng.newvideo:id/video_detail_desc"
video_play_count_id = "com.ifeng.newvideo:id/video_detail_play_count"


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
    if play_count<10000:
        expect_play_count = play_count
        expect_play_message = "{}次播放".format(expect_play_count)
    elif play_count<9999000:
        expect_play_count = '%.1f' % (play_count/10000)
        expect_play_message = "{}万次播放".format(expect_play_count)
    else:
        expect_play_message = "999.9万次播放"
    assert expect_play_message==play_message,'点播视频播放次数不符合规则'
