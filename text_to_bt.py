import jieba

from tools.primitive_mapping import *

BT_SAVE_DIR = "primitives/task_base/"
IMG_BT_SAVE_DIR = "primitives/task_base/images/"
BT_SAVE_DIR_TEMP = "primitives/task_base/temp/"

"""
    已经实现：
"""
# 1 特定句式的 受限自然语言 转换为 行为树
# 2 XML的生成和加载，并成功生成行为树
# 3 人机交互界面实现：实时接受语音信息，触发唤醒词，接受任务描述，转换并显示行为树，保存行为树。
# 3 条件情况的实现
# 4 具体UE环境的搭建


"""
    待解决的问题和要优化的点：
"""

# 1 具体任务的布局
# 2 基元映射和组合的规则完善。 遇到模糊不清的，可以使用概率随机。  重点！！
# 3 流式语音识别的问题：1 只能选中文模型 或者 英文模型，中文模型无法翻译为英文。 2 不能完全使用语音交互，需要点击按钮才能读取完整的一句话实现行为树生成
# 4 UE AI智能体对行为树的实现
# 5 xml格式优化
# 6 语义歧义消除： 定制语义歧义消除模板函数
# 7 jieba对行为树关键节点和关键词的分词定制优化  等待

# 8 论文点：从人机交互的角度来看，人们更偏向于使用重复受限的语言来描述同一个任务
# 9 重用库映射匹配优化：除了存放具体任务的行为树，还要放置对应行为树的 word2vec 向量。之后重用这个行为树可以根据语义来匹配（相似程度XX之后可以使用）
# 10 指代问题（默认已经解决）
# 11 重用库如何抽象存储 以及 可重用行为树本身的优化。


def replace_bt_by_reverse_find(bt, primitive):
    """
        倒顺序查找list进行子树的链接
    """
    stack = [bt]
    while stack:
        node = stack.pop()
        for child in node.children:
            stack.append(child)
            if child.name == primitive.name + "Index":
                child.parent.replace_child(child, primitive)
                return bt
    return bt


def replace_bt_by_index(bt, location, primitive):
    """
        根据指定的具体位置替换基元
    """
    layer = location[0]
    position = location[1]
    if not bt:
        return None
    if layer == 1 and position == 1:  # 如果要替换的位置是第一个，则直接返回这个基元
        return primitive

    queue = [bt]
    cur_level = 1
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.pop(0)
            if cur_level == layer and i + 1 == position:
                node.parent.replace_child(node, primitive)
                return bt
            for child in node.children:
                queue.append(child)
        cur_level += 1

    return None


def create_control_index(bt):
    """
        遍历一个树，并且返回符合Index的每个位置
    """
    # 根据control_node_base获得带有所有控制节点作为key的字典
    control_index_dict = create_control_index_list()
    # 定义结果列表和当前层数
    cur_layer = 1

    # 定义深度优先遍历函数
    def dfs(node, layer, location):
        # 如果当前节点为空，直接返回
        if not node:
            return
        # 如果该节点带有Index，将当前节点的位置信息添加到结果列表中
        if "Index" in node.name:
            control_index_dict[node.name].append([layer, location])
        # 遍历当前节点的子节点
        for i, child in enumerate(node.children):
            # 递归遍历子节点
            dfs(child, layer + 1, i + 1)

    # 从根节点开始遍历
    dfs(bt, cur_layer, 0)
    # 返回结果列表
    return control_index_dict


def combine_bt(primitive, bt, combine_rule=None):
    """
        组合：链接当前子树和总行为树。          待优化

        组合情况判断：
            有无 ControlIndex
                有, 遍历一遍所有节点，为同名 ControlIndex 递增编号放入相应数组中。：
                        例：{
                                parallelIndex: [[第几层，从1开始, 第几个位置，从1开始],[1,3],[2,4]]
                                sequenceIndex: [[1,1],[3,5]]
                                parallelIndex: []
                            }
                    如果数量只有一个：
                        直接将当前 primitive 加入到 bt 这个Index中
                    如果数量有多个，查询语句中是否有明确位置关系的描述：
                        有：
                            分析这个位置，对应然后链接成功

                        无：
                            调用语义歧义消除函数，询问加入到哪个位置
                无：
                    说明总树已经完成（就是一个 task 节点。或者是一个没有控制节点不断生成的树）。
                    反馈用户说没有连接索引，问是否先执行这个行为树。问用户满意不，然后保存这个行为树。然后在建立一颗新的行为树。
    """
    if primitive is None or bt is None:
        return None

    # 得到总行为树的Index字典
    control_dict = create_control_index(bt)

    # 获取当前 primitive 的头节点名称,加上Index与之对应
    key_name = primitive.name + "Index"

    control_index_list = control_dict[key_name]
    # 有对应 primitive 的index。需要进行组合
    if control_index_list is not None:
        # index数量只有一个，直接进行拼接
        index_number = len(control_dict[key_name])
        if index_number == 1:
            location = control_index_list[0]
            replace_bt_by_index(bt, location, primitive)
            return bt
        else:  # index的数量有多个，根据组合规则进行判断. 暂时只按顺序拼接
            bt = replace_bt_by_reverse_find(bt, primitive)
            return bt
    else:  # 没有index，说明不需要组合。有可能是新的任务。也有可能是描述不清楚导致歧义
        pass

    return bt


def create_primitive(seg_list, rule):
    """
        基元生成：根据一句话创建基元的方法, 返回这个树的根节点。     待优化
    """
    primitive = None  # 基元
    # rule0：按顺序读取关键词
    for word in seg_list:
        print(word)
        # node_str  具体的基元名称
        # node_type 基元的类型 (-1: None) (0: task) (1: action) (2: control)
        node_str, node_type = find_node_type(word)
        if node_str is not None:
            if primitive is not None:
                # 如果是control节点添加一个索引位置；如果是 action 或 task 直接添加该节点
                if node_type == 0:  # 任务节点
                    task_node = create_BT_node(node_str)
                    primitive.add_child(task_node)
                elif node_type == 1:  # action节点
                    action_node = create_BT_node(node_str)
                    primitive.add_child(action_node)
                elif node_type == 2:  # 控制节点，添加索引
                    control_node = create_BT_node(node_str)
                    control_node.name = control_node.name + "Index"
                    primitive.add_child(control_node)
                else:
                    pass
                    # 无法解析，调用语义歧义消除模块
                    # primitive_generate_disambiguation()
            else:
                # 行为树根节点
                root_node = create_BT_node(node_str)
                primitive = root_node
    return primitive


def select_combine_rule(tasks):
    """
        句型，依存分析，语义抽象程度 等判断： 以便决定使用哪种 基元生成规则 和 组合规则(rule：规则->1,2,3...)     待优化
        具体情况判断： 语言是否无歧义。对每个节点都有数字标注，比如创建两个顺序节点，第一个是A，第二个是B           待优化
    """

    return 0, 1


def text_to_BT(all_text, bt=None):
    """
        任务自然语言描述到行为树的总函数
    """
    # 1 语句以句号作为一个节点的生成, 每一句话都是一个子树基元
    task_list = re.split(r"[.。!！]", all_text)
    # 2 选择基元生成规则和组合规则
    primitive_rule, combine_rule = select_combine_rule(task_list)

    # 3 每一次循环产生一个基元任务
    for sub_task in task_list:
        sub_task_seg_list = jieba.cut(sub_task)
        # 4 对任务进行基元构建
        primitive = create_primitive(sub_task_seg_list, primitive_rule)
        # 5 判断是否之前已经有行为树, 有就尝试链接
        if bt is None:
            bt = primitive
        else:
            combine_bt(primitive, bt, combine_rule)
    return bt


if __name__ == '__main__':
    #                                                第一轮
    print("第 一 轮")
    # 触发词，唤醒词
    print("我在，请问想要我做什么？")

    task = "同时进行顺序任务和选择任务和顺序任务."
    print(task)
    BT = text_to_BT(task)
    print(py_trees.display.unicode_tree(BT))  # 每句话完成进行行为树的反馈
    tree_to_xml_file(BT, "temp", BT_SAVE_DIR_TEMP + 'temp.xml')

    task = "顺序任务进行action1,action2,action1action1和顺序任务."
    print(task)
    BT = text_to_BT(task, BT)
    print(py_trees.display.unicode_tree(BT))

    task = "选择任务进行action3,action4."
    print(task)
    BT = text_to_BT(task, BT)
    print(py_trees.display.unicode_tree(BT))

    task = "顺序任务进行action2,action1."
    print(task)
    BT = text_to_BT(task, BT)
    print(py_trees.display.unicode_tree(BT))

    task = "顺序任务中，如果发生了A，那么执行action5，action6."
    print(task)
    BT = text_to_BT(task, BT)
    print(py_trees.display.unicode_tree(BT))

    # 判断是否该任务是否结束？ 结束就命名，并且保存到库中
    print("为了之后利用它，请给本次任务命名：")
    task_name = "test"
    tree_to_xml_file(BT, task_name, BT_SAVE_DIR + task_name + '.xml')
    dir_path = IMG_BT_SAVE_DIR + task_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    py_trees.display.render_dot_tree(BT, name=task_name, target_directory=IMG_BT_SAVE_DIR + task_name)

    BT = xml_file_to_tree(BT_SAVE_DIR + task_name + '.xml')
    print(py_trees.display.unicode_tree(BT))

    #                                                     第二轮
    print("第 二 轮")
    # 触发词，唤醒词
    print("我在，请问想要我做什么？")

    task = "顺序进行顺序任务和test."
    print(task)
    BT = text_to_BT(task)
    print(py_trees.display.unicode_tree(BT))

    task = "顺序任务执行action1和action2."
    print(task)
    BT = text_to_BT(task, BT)
    print(py_trees.display.unicode_tree(BT))

    print("为了之后利用它，请给本次任务命名：")
    task_name = "test2"
    tree_to_xml_file(BT, task_name, BT_SAVE_DIR + task_name + '.xml')
    dir_path = IMG_BT_SAVE_DIR + task_name
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    py_trees.display.render_dot_tree(BT, name=task_name, target_directory=IMG_BT_SAVE_DIR + task_name)

    BT = xml_file_to_tree(BT_SAVE_DIR + task_name + '.xml')
    print(py_trees.display.unicode_tree(BT))

    # 1设置唤醒词

    wake_word = "11"  # 机器人唤醒
    end_word = "任务描述结束"  # 任务描述结束定义
    start_action_word = "action"  # 任务执行

    # 2语音识别器定义

    # 3开始循环
    while False:
        # 4 语音识别一直监听，得到语音
        print("Say something!")

        try:
            # 5 识别语音并获取文本
            text = "12  "
            print("something is ...")

            # 6 检查是否检测到唤醒词
            if wake_word in text.lower():
                print("我在，请问想要我做什么？")
                # 7 任务描述，在没有听到任务结束，或者结束任务时，等待下一个语句进行行为树合并
                describe_end = False
                while not describe_end:
                    task = "顺序进行顺序任务和test."
                    print(task)
                    BT = text_to_BT(task)
                    print(py_trees.display.unicode_tree(BT))  # 将行为树反馈到交互界面中
                    # 8 任务描述结束判断
                    print("任务描述结束判断")
                    describe_end = False
                    if describe_end:  # 任务描述结束
                        # 9 开始执行的触发词
                        print("开始执行任务")
                        # 10 任务重用逻辑
                        print("为了之后利用它，请给本次任务命名：")
                        task_name = "test2"
                        tree_to_xml_file(BT, task_name, BT_SAVE_DIR + task_name + '.xml')
                        dir_path = IMG_BT_SAVE_DIR + task_name
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)
                        py_trees.display.render_dot_tree(BT, name=task_name,
                                                         target_directory=IMG_BT_SAVE_DIR + task_name)
        except Exception as e:
            print("could not understand audio")
