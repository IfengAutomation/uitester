# @Time    : 2016/11/11 11:01
# @Author  : lixintong
from keywords import keyword, var_cache


@keyword('current_activity')
def current_activity(acticity_desc):
    """
    :param acticity_desc:video_player or topic_player or live or vr_live or pic_player or local_player
    :return:
    """
    return var_cache['proxy'].current_activity(acticity_desc)


@keyword('change_video_state')
def change_video_state(player_name, state):
    """
    :param player_name: player_name or topic_player or live or pic_player or local_player
    :param state: play or pause
    :return:
    """
    return var_cache['proxy'].change_video_state(player_name, state)
