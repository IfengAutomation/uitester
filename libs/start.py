
from keywords import keyword, get_var
from solo import UIDevice, InstrumentationRegistry


@keyword('scroll_into_main')
def scroll_into_main():
    """
    滑动欢迎页
    进入首页
    :return:
    """
    # 滑动四个欢迎页
    import time
    time.sleep(2)
    solo = get_var("solo")
    i = 0
    for i in range(4):
        solo.scroll_to_right()


@keyword('scroll_click_into_main')
def scroll_click_into_main():
    """
    滑动欢迎页，点击立即体验进入首页
    :return:
    """
    solo = get_var("solo")
    import time
    time.sleep(2)
    i = 0
    for i in range(3):
        solo.scroll_to_right()
    # TODO click activity
    solo.click_on_screen(510, 1590)


@keyword('back_reopen')
def back_reopen(wait_time=0):
    """
    模拟按下home键, 置于后台，等待指定时间后再重新唤醒
    :param wait_time:指定等待时间 默认为0
    :return:
    """
    instrumentation = InstrumentationRegistry.get_instrumentation()
    context = instrumentation.get_target_context()
    ui_device = UIDevice.get_instance(instrumentation)
    ui_device.press_home()
    import time
    if wait_time:
        time.sleep(int(wait_time))
    intent = context\
        .get_package_manager() \
        .get_launch_intent_for_package("com.ifeng.newvideo")
    context.start_activity(intent)


@keyword('scroll_channel_right')
def scroll_channel_right():
    """
    向右滑动顶部频道
    :return:
    """
    solo = get_var("solo")
    top_channel_view = solo.get_view("com.ifeng.newvideo:id/top_slide_tab_main")
    solo.scroll_view_to_right(top_channel_view)


@keyword('scroll_channel_left')
def scroll_channel_left():
    """
    向左滑动顶部频道
    :return:
    """
    solo = get_var("solo")
    top_channel_view = solo.get_view("com.ifeng.newvideo:id/top_slide_tab_main")
    solo.scroll_view_to_left(top_channel_view)
