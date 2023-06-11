from bt_builder.builder import *
from bt_disambiguator.disambiguator import *


def create_level1_bt_list(sent):
    """
    由于级别1的语言没有歧义，并且和行为树节点一一对应。
    直接按照顺序读取句子，提取所有与 行为树库 重名或者相似的节点
    :param sent: 行为树节点描述级语言
    :return: 行为树节点列表
    """
    bt_list = []
    # TODO: 1 分词
    words = jieba.cut(sent, cut_all=False)
    for word in words:
        # 如果为空、空格或者是符号等，直接跳向下一个词
        pattern = r'^[\s\W]+$'
        if word is None or len(word) == 0 or word == " " or bool(re.match(pattern, word)):
            continue
        # TODO: 2 根据分词查找行为树节点
        node_name, node_type = find_bt(word)
        if node_name is None or node_type == -1:
            continue
        # TODO: 3 将行为树信息保存到列表中
        bt_info = {"name": node_name, "type": node_type}
        bt_list.append(bt_info)
    # TODO: 4 错误判断
    if bt_list is None or len(bt_list) == 0:
        return None, "ERROR: No valid behavior tree node identified for '" + sent + "' !!"
    else:
        return bt_list, "SUCCESS"
