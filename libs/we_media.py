# @Time    : 2016/11/17 10:58
# @Author  : lixintong
from keywords import keyword
from player import check_view_exist, click_view, get_view_by_id, get_text_by_id, change_to_bool, sleep

media_container_id = "com.ifeng.newvideo:id/video_detail_media_container"
detail_follow_id = "com.ifeng.newvideo:id/video_detail_follow"


@keyword("check_media_container_exits")
def check_media_container_exits(expect_result):
    check_view_exist(media_container_id, expect_result)


@keyword("click_media_container_view")
def click_media_container_view():
    click_view(media_container_id)


@keyword("check_media_state")
def check_media_state(state,expect_result):
    sleep(2000)
    text = get_text_by_id(detail_follow_id)
    result = text == state
    expect_result = change_to_bool(expect_result)
    assert result == expect_result, "check_media_state 实际与期望不符"
