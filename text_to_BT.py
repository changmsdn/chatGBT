import jieba
from tools.XML_trans import *

BT_SAVE_DIR = "primitives/task_base/"
IMG_BT_SAVE_DIR = "primitives/task_base/Img/"

# 要优化的点：
# 1 组合的规则，遇到模糊不清的，可以使用概率随机
# 2 重用库，重用库除了存放具体任务的行为树，还要放置一个行为树对应的 word2vec 向量。之后重用这个行为树可以根据语义来匹配（相似程度XX之后可以使用）
# 3 受限自然语言的补充。
# 4 具体任务的布局
# 5 指代问题和歧义问题
# 6 增加条件的情况。 如果....则...

# 具体项目：（环境搭建好）
# 1 人工智能AI行为树的构建

# 根据一句话创建基元的方法, 返回这个树的根节点以及排列的list
def create_sub_tree(seg_list):
    sub_BT = None  # 行为树
    for word in seg_list:
        print(word)
        # node_str 返回具体的节点名称
        # node_type:  (-1: None) (0: task) (1: action) (2: control)
        node_str, node_type = find_node_type(word)
        if node_str is not None:
            if sub_BT != None:
                # 如果是控制节点，添加一个索引位置，如果是行为节点直接添加
                if node_type == 0:
                    task_node = create_node(node_str)
                    sub_BT.add_child(task_node)
                elif node_type == 1:
                    action_node = create_node(node_str)
                    sub_BT.add_child(action_node)
                elif node_type == 2:  # 控制节点，添加索引
                    control_node = create_node(node_str)
                    control_node.name = control_node.name + " Index"
                    sub_BT.add_child(control_node)
                else:
                    pass
            else:
                # 行为树根节点
                node = create_node(node_str)
                sub_BT = node
    return sub_BT


# 倒顺序查找list进行子树的链接
def link_tree(sub_BT, BT_node):
    if sub_BT == None or BT_node == 0:
        return None

    # 递归终止条件
    if not BT_node:
        return

    # 先遍历所有子节点
    for child in BT_node.children[::-1]:
        link_tree(sub_BT, child)

    # 输出当前节点的值, 判断当前节点是否是子树根节点
    if BT_node.name == sub_BT.name + " Index":
        # 将原来的索引节点改成真实的节点, 遍历它的父亲节点，然后找到对应的索引替换
        for index, child in enumerate(BT_node.parent.children):
            if child.name == sub_BT.name + " Index":
                BT_node.parent.children[index] = sub_BT
                return BT
    return BT


# 任务自然语言描述到行为树的总函数
def text_to_tree(task, BT=None):
    # 1 语句以句号作为一个节点的生成, 每一句话都是一个子树基元
    tasks = re.split(r"[.。]", task)
    # 2 每一次循环产生一个基元任务
    for task in tasks:
        seg_list = jieba.cut(task)
        # 3 对任务进行子树构建
        subBT = create_sub_tree(seg_list)
        # 4 判断是否有父节点,有就链接
        if BT == None:
            BT = subBT
        else:
            link_tree(subBT, BT)  # 当前生成的行为树结合总行为树
    return BT


if __name__ == '__main__':
    #                                                第一轮
    print("第 一 轮")
    # 触发词，唤醒词
    print("我在，请问想要我做什么？")

    task = "同时进行顺序任务和选择任务."
    print(task)
    BT = text_to_tree(task)
    print(py_trees.display.unicode_tree(BT))  # 每句话完成进行行为树的反馈

    task = "顺序任务进行action1,action2,action1action1和顺序任务."
    print(task)
    BT = text_to_tree(task, BT)
    print(py_trees.display.unicode_tree(BT))

    task = "选择任务进行action3,action4."
    print(task)
    BT = text_to_tree(task, BT)
    print(py_trees.display.unicode_tree(BT))

    task = "顺序任务执行action5和action6."
    print(task)
    BT = text_to_tree(task, BT)
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
    BT = text_to_tree(task)
    print(py_trees.display.unicode_tree(BT))

    task = "顺序任务执行action1和action2."
    print(task)
    BT = text_to_tree(task, BT)
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
