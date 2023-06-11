from bt_instruction2bt_mapper.bt_tools import *
from bt_builder.level1_parser import *
from bt_builder.level2_parser import *
from bt_builder.level3_parser import *


def create_bt_list(sent, level):
    """
    根据针对行为树描述不同语言级别一句话 生成这个句子中所有可能的行为树节点列表
    :param level: 句子对于行为树的抽象级别
    :param sent: 包含三种等级之一的受限自然语言
    :return: 行为树节点列表
    """
    if level == 1:
        # TODO: 1 "行为树描述级"的自然语言将会和所有的节点同名。按顺序搜索即可。
        bt_list, status_info = create_level1_bt_list(sent)
    elif level == 2:
        # TODO: 2 "流程描述级"的自然语言先使用初始定义的规则解析。不够就用大模型，大模型的知识将会被重用到规则中。
        bt_list, status_info = create_level2_bt_list(sent)
    else:
        # TODO: 3 "任务描述级"的自然语言直接搜索重用节点。不够就用大模型根据任务本身和机器人能力规划任务，并且重用到规则中。
        bt_list, status_info = create_level3_bt_list(sent)
    return bt_list, status_info
