import jieba
from tools.xml_trans import *

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

# 7 论文点：从人机交互的角度来看，人们更偏向于使用重复受限的语言来描述同一个任务
# 8 重用库映射匹配优化：除了存放具体任务的行为树，还要放置对应行为树的 word2vec 向量。之后重用这个行为树可以根据语义来匹配（相似程度XX之后可以使用）
# 9 指代问题（默认已经解决）
# 10 重用库如何抽象存储 以及 可重用行为树本身的优化。


def combine_BT(primitive, BT, combine_rule):
    """
        组合：链接当前子树和总行为树。          待优化
    """
    if primitive == None or BT == 0:
        return None
    # 倒顺序查找list进行子树的链接
    # 递归终止条件
    if not BT:
        return

    # 先遍历所有子节点
    for child in BT.children[::-1]:
        combine_BT(primitive, child, combine_rule)

    # 输出当前节点的值, 判断当前节点是否是子树根节点
    if BT.name == primitive.name + "Index":
        # 将原来的索引节点改成真实的节点, 遍历它的父亲节点，然后找到对应的索引替换
        for index, child in enumerate(BT.parent.children):
            if child.name == primitive.name + "Index":
                BT.parent.children[index] = primitive
                return BT
    return BT


def create_primitive(seg_list, rule):
    """
        基元生成：根据一句话创建基元的方法, 返回这个树的根节点。     待优化
    """
    primitive = None  # 基元
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
            else:
                # 行为树根节点
                root_node = create_BT_node(node_str)
                primitive = root_node
    return primitive


def select_combine_rule(tasks):
    """
        句型，依存分析，语义抽象程度 等判断： 以便决定使用哪种 基元生成规则 和 组合规则(rule：规则->1,2,3...)     待优化
    """
    return 0, 1


def text_to_BT(text, BT=None):
    """
        任务自然语言描述到行为树的总函数
    """
    # 1 语句以句号作为一个节点的生成, 每一句话都是一个子树基元
    tasks = re.split(r"[.。]", text)
    # 2 选择基元生成规则和组合规则
    primitive_rule, combine_rule = select_combine_rule(tasks)

    # 3 每一次循环产生一个基元任务
    for task in tasks:
        seg_list = jieba.cut(task)
        # 3 对任务进行基元构建
        primitive = create_primitive(seg_list, primitive_rule)
        # 4 判断是否有父节点,有就链接
        if BT is None:
            BT = primitive
        else:
            combine_BT(primitive, BT, combine_rule)  # 当前生成的行为树结合总行为树
    return BT


if __name__ == '__main__':
    #                                                第一轮
    print("第 一 轮")
    # 触发词，唤醒词
    print("我在，请问想要我做什么？")

    task = "同时进行顺序任务和选择任务."
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
