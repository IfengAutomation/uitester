# @Time    : 2016/11/14 16:46
# @Author  : lixintong
from keywords import keyword, get_var, call

pic_channel_comment_id = "com.ifeng.newvideo:id/tv_channel_big_pic_comment"


@keyword("play_pic_channel_video")
def play_pic_channel_video(index):
    """
    播放大图频道的第n个视频
    :param index:第n个视频
    :return:
    """
    solo = get_var("solo")
    solo.sleep(3000)
    view = solo.get_view(res_id="com.ifeng.newvideo:id/iv_channel_big_pic_play_status", index=int(index))
    solo.click_on_view(view)


@keyword("click_pic_channel_comment")
def click_pic_channel_comment(index="0"):
    solo = get_var("solo")
    solo.sleep(3000)
    view = solo.get_view(res_id=pic_channel_comment_id, index=int(index))
    solo.click_on_view(view)


@keyword("check_pic_channel_comment_count")
def check_pic_channel_comment_count(index, expect_text=""):
    solo = get_var("solo")
    solo.sleep(3000)
    view = solo.get_view(res_id=pic_channel_comment_id, index=int(index))
    result_text = call(view, "getText")
    assert result_text == expect_text, "评论展示不一致"




