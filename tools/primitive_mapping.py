import py_trees
import os
import re
import xml.etree.ElementTree as ET
import condition
import action

Dir_action_node_base = "primitives/action_node_base"
Dir_control_node_base = "primitives/control_node_base"
Dir_task_base = "primitives/task_base"


def find_in_task_base(dir, word):
    """
        判断 word 是否匹配 task
    """
    for filename in os.listdir(dir):  # 遍历给定文件夹中的所有文件
        file_path = os.path.join(dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.xml'):
            # 打开XML文件并解析为 ElementTree
            tree = ET.parse(file_path)
            root = tree.getroot().getchildren()[0]
            if root.get("name") == word:
                return root.get("name")
    return None


def find_in_action_node_base(dir, word):
    """
        判断 word 是否匹配 action
    """
    # 遍历给定文件夹中的所有文件
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.xml'):
            tree = ET.parse(file_path)
            root = tree.getroot().getchildren()[0]
            for element in root.iter():
                if element.get("name") == word:
                    return root.get("name")
    return None


def find_in_control_node_base(dir, word):
    """
        判断 word 是否匹配 control
    """
    # 遍历给定文件夹中的所有文件
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        if os.path.isfile(file_path) and filename.endswith('.xml'):
            # 打开XML文件并解析为 ElementTree
            tree = ET.parse(file_path)
            root = tree.getroot().getchildren()[0]  # 忽略第一个根节点
            # 遍历所有元素，查找具有相同标记值的节点, 返回xml文件的根名
            for element in root.iter():
                if element.get("name") == word:
                    return root.get("name")
    # 如果没有找到相同标记值的节点，则返回None
    return None


def find_node_type(word):
    """
        找到 word 匹配 primitive， 返回 primitive标记 和 primitive类型
    """
    # 如果word是符号或者是空，则返回空
    pattern = r'^[^a-zA-Z0-9\u4e00-\u9fa5]+$'
    if word == None or len(word) == 0 or bool(re.match(pattern, word)):
        return None, -1  # word什么都不是

    # 遍历查找，先查找action_node_base, 然后查找control_node_base，然后查找task_base
    task_str = find_in_task_base(Dir_task_base, word)
    if task_str != None:
        return task_str, 0  # word是task，用 0 表示

    action_str = find_in_action_node_base(Dir_action_node_base, word)
    if action_str != None:
        return action_str, 1  # word是action，用 1 表示

    control_str = find_in_control_node_base(Dir_control_node_base, word)
    if control_str != None:
        return control_str, 2  # word是control，用 2 表示
    return None, -1


def get_task_base_list():
    """
        查找重用库 task_base 的所有任务， 返回任务列表
    """
    task_base_list = {}
    for file_name in os.listdir(Dir_task_base):
        if os.path.isfile(os.path.join(Dir_task_base, file_name)):
            file_name = os.path.splitext(file_name)[0]
            task_base_list[file_name] = os.path.join(Dir_task_base, file_name)
    return task_base_list


def create_BT_node(node_str):
    """
        根据名字在 primitives 中查找，存在则创建。
    """
    if "parallel" in node_str:
        return py_trees.composites.Parallel(name=node_str, policy=py_trees.common.ParallelPolicy.Base)
    if "sequence" in node_str:
        return py_trees.composites.Sequence(name=node_str, memory=False)
    if "selector" in node_str:
        return py_trees.composites.Selector(name=node_str, memory=False)
    if "action1" in node_str:
        return action.Action1(name=node_str)
    if "action2" in node_str:
        return action.Action2(name=node_str)
    if "action3" in node_str:
        return action.Action3(name=node_str)
    if "action4" in node_str:
        return action.Action4(name=node_str)
    if "action5" in node_str:
        return action.Action5(name=node_str)
    if "action6" in node_str:
        return action.Action6(name=node_str)
    if "condition1" in node_str:
        return condition.Condition1(name=node_str)
    if "condition2" in node_str:
        return condition.Condition2(name=node_str)
    task_base_list = get_task_base_list()
    for task_name, dir in task_base_list.items():
        if task_name == node_str:
            return xml_file_to_tree(dir + '.xml')
    return None


def xml_file_to_tree(file_path):
    """
        从XML文件中读取树形结构并返回根节点
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        # 从文件中读取XML数据并创建根元素
        task_root = ET.fromstring(f.read()).getchildren()[0].getchildren()[0]
        # 将XML元素转换为树形结构节点
        tree = convert_element(task_root)
    return tree


def convert_element(element):
    """
        将XML元素转换为树形结构节点
    """
    # 如果是控制节点或者是action，那么创建节点
    BT = create_BT_node(element.get("name"))
    for child_element in element:
        BT.add_child(convert_element(child_element))
    return BT
