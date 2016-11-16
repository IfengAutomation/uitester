# @Time    : 2016/11/14 16:46
# @Author  : lixintong
from keywords import keyword, get_var


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
