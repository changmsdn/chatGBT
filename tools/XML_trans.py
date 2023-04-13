from tools.node_mapping import *


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
    xml_node = ET.Element(node.name, {"name": node.name})
    # 将XML元素添加到父元素中
    parent.append(xml_node)
    # 递归处理所有子节点
    for child in node.children:
        convert_node(child, xml_node)


# 从XML文件中读取树形结构并返回根节点
def xml_file_to_tree(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # 从文件中读取XML数据并创建根元素
        task_root = ET.fromstring(f.read()).getchildren()[0].getchildren()[0]

        # 将XML元素转换为树形结构节点
        tree = convert_element(task_root)
    return tree


# 将XML元素转换为树形结构节点
def convert_element(element):
    # 如果是控制节点或者是action，那么创建节点
    BT = create_node(element.get("name"))
    for child_element in element:
        BT.add_child(convert_element(child_element))
    return BT
