import re
import xml.etree.ElementTree as ET
from bt_instruction2bt_mapper.bt_tools import *
from llm import llm


def get_level1_combine_prompt(bt_list, sent):
    prompt = f"""
Given a command natural language sent and the corresponding behavior tree list bt_list, help me generate an xml file.

Example:
input: sent and bt_list
sent: "Create a sequence node and add child nodes cleaning_tool_detection, clean_area_detection, and check_cleanliness"
bt_list: [{{'name': 'sequence', 'type': 1}}, {{'name': 'cleaning_tool_detection', 'type': 2}}, \
{{'name': 'clean_area_detection', 'type': 2}} , {{'name': 'check_cleanliness', 'type': 3}}]
output:
<rule>
     <pattern>(Create|Generate|Execute|Produce|Add).*(with child nodes|add the child nodes).*</pattern>
     <code>
def get_bt(bt_list):
     root = None
     for bt in bt_list:
         if root is None:
             root = create_bt_node(bt['name'])
         else:
             node = create_bt_node(bt['name'])
             root.add_child(node)
     return root, "SUCCESS"
bt, status_info = get_bt(bt_list)
     </code>
</rule>

Illustrate:
"pattern": conforms to the regular expression of the input "sent", \
and has generality about sentence patterns or behavior trees.
"code": According to the content of this sentence and pattern, \
give the code in the combined bt_list node. \
Make the combined behavior tree conform to the semantic intention of the "sent".
"bt_list": bt_list is a list of specific behavior trees for each intent \
after decomposition according to regular expressions "pattern".
"create_bt_node": A behavior tree node can be generated according to \
the nouns of each dictionary in bt_list.

Require:
- Only generate xml results, do not print redundant instructions

input:
sent: "{sent}"
bt_list: {bt_list}
output:
    """
    return prompt


def combine_level1_bt(bt_list, sent):
    """
    根据文件的 正则表达式 规则，加载并执行相应的组合代码，得到组合后的行为树
    :param bt_list: 从自然语言按顺序读入的 bt节点
    :param sent: 行为树描述级的自然语言
    :return: 行为树
    """
    # TODO: 1 读取 level1_combine_rules.xml。获取相应 python代码，并且生成具体的行为树。
    filename = dir_root + "bt_composition_planner/level1_combine_rules.xml"
    tree = ET.parse(filename)
    root = tree.getroot()
    rules = root.findall("rule")
    bt = None
    status_info = None
    for rule in rules:
        pattern = rule.find("pattern").text
        code = rule.find("code").text
        pattern = re.compile(pattern, re.IGNORECASE)
        if re.match(pattern, sent):
            namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
            exec(code, namespace)
            bt = namespace['bt']
            status_info = namespace['status_info']
            break
    if status_info == "SUCCESS":
        return bt, status_info
    # TODO: 2 所有规则都无法匹配，调用大模型，针对该句添加规则到配置文件 level1_combine_rules.xml 中
    else:
        # TODO: 2.1 调用大模型生成对应的正则表达式和代码
        prompt = get_level1_combine_prompt(bt_list, sent)
        result_xml = llm.get_completion(prompt)
        print(result_xml)
        flag = False
        for i in range(5):
            root = ET.fromstring(result_xml)
            pattern = root.find("pattern")
            match = re.search(pattern.text, sent, re.IGNORECASE)
            if not match:
                continue
            code = root.find("code")
            namespace = {'bt_list': bt_list, 'create_bt_node': create_bt_node}
            exec(code.text, namespace)
            bt = namespace['bt']
            status_info = namespace['status_info']
            if bt is not None and status_info == "SUCCESS":
                flag = True
                break
        # TODO: 2.2 如果正确匹配和生成行为树，则将这个规则保存到xml文件中
        if flag:
            with open(filename, 'r') as file:
                lines = file.readlines()
            # 找到最后一个非空行的索引
            last_non_empty_line = next((i for i, line in reversed(list(enumerate(lines))) if line.strip()), None)
            # 如果找到了非空行，那么就将其删除
            if last_non_empty_line is not None:
                del lines[last_non_empty_line]
            # 写入新的行
            lines.append(result_xml)
            lines.append("</root>\n")
            # 将新的内容写入文件
            with open(filename, 'w', encoding="utf-8") as file:
                file.writelines(lines)
            return bt, status_info
        else:
            return None, "ERROR: The behavior tree cannot be generated correctly, \
            please give a more detailed behavior tree! '"+sent+"'"
