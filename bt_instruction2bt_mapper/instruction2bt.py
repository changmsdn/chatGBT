from bt_builder.builder import *
from bt_composition_planner.composition import *


def instruction_to_bt(task_desc, all_bt=None):
    """
    根据 任务描述 得到 行为树
    :param task_desc: 任务描述
    :param all_bt: 需要拼接的行为树
    :return: 具体行为树, 状态描述(Success 或 错误描述)
    """
    # TODO: 1 分句
    doc = nlp_en_sm(task_desc)
    status_desc = None
    bt = None
    for sent in doc.sents:
        # 将句子全部小写
        sent = sent.text.lower().strip(" '!,，.。?")
        print("Input sent: " + sent)
        # TODO：2 判断句子等级
        # NOTE: 用一个分类模型改写。三个级别中的一个 或者根本就不是命令
        level = get_language_level(sent)
        print("Sent level: " + str(level))
        if level == -1:
            continue
        # TODO: 3 解析句子，得到与之对应的所有需要用到的 行为树节点列表
        # NOTE: 只要涉及用语义相似度向量计算的，效果都不是很好。没有使用大模型来判断的好。
        bt_list, status_desc = create_bt_list(sent, level)
        print("bt_list: " + str(bt_list))
        # 成功得到 行为树节点列表
        if status_desc == "SUCCESS":
            # TODO: 4 根据 行为树节点列表 和 句子 进行节点组合的分析，并且返回行为树
            sub_bt, status_desc = combine_bt_nodes(bt_list, sent, level)
            # TODO: 5 和之前句子生成的行为树 bt 进行组合
            if bt is not None:
                bt, status_desc = combine_between_bts(sub_bt, bt, sent)
                if status_desc != "SUCCESS":
                    return all_bt, status_desc
            else:
                bt = sub_bt
        else:
            return all_bt, status_desc
    # TODO:6 是否需要和之前的 总行为树进行 组合。
    # NOTE: 是重新执行另一个行为树 还是拼接 也是个问题
    if all_bt is not None:
        all_bt, status_desc = combine_between_bts(bt, all_bt)
        # 成功组合行为树
        if status_desc == "SUCCESS":
            return all_bt, status_desc
        else:
            return all_bt, status_desc
    else:
        return bt, status_desc
