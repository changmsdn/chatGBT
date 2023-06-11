import os
from bt_composition_planner.level1_parser import *
from bt_composition_planner.level2_parser import *
from bt_composition_planner.level3_parser import *


def get_combine_between_bts_prompt(sub_bt, bt, sent):
    pass


def combine_between_bts(sub_bt, bt, sent):
    """
    根据两个行为树进行拼接
    :param sub_bt: 当前生成的行为树
    :param bt: 之前的行为树
    :param sent: 当前生成这颗行为树对应的自然语言
    :return:
    """

    pass


def combine_bt_nodes(bt_list, sent, level):
    """
    根据行为树节点，句子和等级生成一颗具体的行为树
    :param bt_list: 根据 sent 成功解析到要使用的 行为树节点
    :param sent: 指令的自然语言
    :param level: 自然语言的语言级别
    :return: 一颗行为树和状态描述
    """
    if level == 1:
        # 行为树描述级： 将会和所有的节点同名。按顺序搜索即可
        bt, status_info = combine_level1_bt(bt_list, sent)
    elif level == 2:
        # 流程描述级：   先使用初始定义的规则解析。不够就用大模型，大模型的知识将会被重用。
        bt, status_info = combine_level2_bt(bt_list, sent)
    else:
        # 任务描述级：   搜索重用节点。不够就用大模型，并且重用
        bt, status_info = combine_level3_bt(bt_list, sent)
    return bt, status_info
