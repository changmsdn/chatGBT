import py_trees
import os
import re
import xml.etree.ElementTree as ET
import condition
import action

DIR_ACTION_NODE_BASE = "primitives/action_node_base"
DIR_CONTROL_NODE_BASE = "primitives/control_node_base"
DIR_TASK_BASE = "primitives/task_base"


def create_control_index_list():
    """
        根据 DIR_CONTROL_NODE_BASE 获取一个字典
    """
    control_index_dict = {}
    for file in os.listdir(DIR_CONTROL_NODE_BASE):
        filename = file.rsplit(".", 1)[0]
        control_index_dict.update({filename+"Index": []})
    return control_index_dict


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


def find_node_type(seg_word):
    """
        找到 word 匹配 primitive， 返回 primitive标记 和 primitive类型
    """
    # 如果word是符号或者是空，则返回空
    pattern = r'^[^a-zA-Z0-9\u4e00-\u9fa5]+$'
    if seg_word is None or len(seg_word) == 0 or bool(re.match(pattern, seg_word)):
        return None, -1  # word什么都不是

    # 遍历查找，先查找action_node_base, 然后查找control_node_base，然后查找task_base
    task_str = find_in_task_base(DIR_TASK_BASE, seg_word)
    if task_str is not None:
        return task_str, 0  # word是task，用 0 表示

    action_str = find_in_action_node_base(DIR_ACTION_NODE_BASE, seg_word)
    if action_str is not None:
        return action_str, 1  # word是action，用 1 表示

    control_str = find_in_control_node_base(DIR_CONTROL_NODE_BASE, seg_word)
    if control_str is not None:
        return control_str, 2  # word是control，用 2 表示
    return None, -1


def get_task_base_list():
    """
        查找重用库 task_base 的所有任务， 返回任务列表
    """
    task_base_list = {}
    for file_name in os.listdir(DIR_TASK_BASE):
        if os.path.isfile(os.path.join(DIR_TASK_BASE, file_name)):
            file_name = os.path.splitext(file_name)[0]
            task_base_list[file_name] = os.path.join(DIR_TASK_BASE, file_name)
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


# 将树形结构转换为XML文件并保存到硬盘中
def tree_to_xml_file(BT, task_name, file_path):
    # 创建根元素
    root = ET.Element('root')
    # 将树形结构转换为XML元素并添加到根元素中
    task_node = ET.SubElement(root, "task", {"name": task_name})
    convert_node(BT, task_node)
    # 创建XML树对象并将其写入硬盘中
    xml_tree = ET.ElementTree(root)
    xml_tree.write(file_path, encoding='utf-8', xml_declaration=True)


# 将树形结构节点转换为XML元素
def convert_node(node, parent):
    # 创建XML元素
    # 如果node.name是以Index结尾的，则标签存入node, 属性name存入nodeIndex
    name = node.name
    if "Index" in name:
        name = name.replace("Index", "")
    xml_node = ET.Element(name, {"name": node.name})
    # 将XML元素添加到父元素中
    parent.append(xml_node)
    # 递归处理所有子节点
    for child in node.children:
        convert_node(child, xml_node)


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
