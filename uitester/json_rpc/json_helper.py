
import json

from uitester.json_rpc.request import Request
from uitester.json_rpc.response import Response


def encode_obj_to_json(obj):
    """
    把对象(支持单个对象、list、set)转换成字典
    :param obj:
    :return:
    """
    end_sign = "\n"     # 结束标记符号
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            # 把Object对象转换成Dict对象
            json_dict = {}
            json_dict.update(o.__dict__)
            json_str = json.dumps(json_dict)
            obj_arr.append(json_str)
        result_str = end_sign.join(obj_arr)
    else:
        json_dict = {}
        json_dict.update(obj.__dict__)
        result_str = json.dumps(json_dict)
    result_str = encode(result_str) + "\n"
    result_bytes = result_str.encode(encoding="utf-8")
    return result_bytes


def decoded_json_to_response(encoded_json):
    return json_to_response_obj(decode(encoded_json))


def json_to_response_obj(json_str):
    """
    将json串转换为Response对象
    :param json_str:
    :return:
    """
    json_dict = json.loads(json_str)  # 将json转化为字典

    res_obj1 = Response(0, "",)
    res_obj1.__dict__ = json_dict  # 将字典转化为ResponseObj对象
    return res_obj1


def decoded_json_to_request(encoded_json):
    return json_to_request_obj(decode(encoded_json))


def json_to_request_obj(json_str):
    """
    将json串转换为Request对象
    :param json_str:
    :return:
    """
    json_dict = json.loads(json_str)  # 将json转化为字典

    # res_obj1 = Request(0, 1, '', '', [])
    res_obj1 = Request()
    res_obj1.__dict__ = json_dict  # 将字典转化为ResponseObj对象
    return res_obj1


def encode(msg):
    """转译，规则为：
        % -> %e
        \n -> %n
    """
    msg = msg.replace("%", "%e")
    msg = msg.replace("\n", "%n")
    return msg


def decode(msg):
    """反转译，规则为：
        %n -> \n
        %e -> %
    """
    msg = msg.replace("%n", "\n")
    msg = msg.replace("%e", "%")
    return msg

