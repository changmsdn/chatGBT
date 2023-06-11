import re
import xml.etree.ElementTree as ET
from bt_instruction2bt_mapper.bt_tools import *
from llm import llm


def get_level3_combine_prompt(bt_list, sent):
    prompt = f"""
Given a command natural language sent and the corresponding behavior tree list bt_list, help me generate an xml file.

Example:
input: sent and bt_list
sent: "Create a sequence node and add child nodes cleaning_tool_detection, clean_area_detection, and check_cleanliness"
bt_list: [{{'name': 'sequence', 'type': 1}}, {{'name': 'cleaning_tool_detection', 'type': 2}}, \
{{'name': 'clean_area_detection', 'type': 2}} , {{'name': 'check_cleanliness', 'type': 3}}]
output:
<rule>
     <sent>Create a sequence node and add child nodes cleaning_tool_detection, \
     clean_area_detection, and check_cleanliness</sent>
     <code>
def get_bt(bt_list):
     root = None
     for bt in bt_list:
         if root is None:
             root = bt_create(bt['name'])
         else:
             node = bt_create(bt['name'])
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
"bt_create": A behavior tree node can be generated according to \
the nouns of each dictionary in bt_list.

Require:
- Only generate xml results, do not print redundant instructions

input:
sent: "{sent}"
bt_list: {bt_list}
output:
    """
    return prompt


def combine_level3_bt(bt_list, sent):
    """
    :param bt_list: 根据 sent 通过 bt_builder 解析出来的需要用到的行为树节点列表
    :param sent: "任务"描述级别的自然语言
    :return: 行为树
    """
    # TODO: 1 读取 level1_combine_rules.xml。获取相应 python代码，并且生成具体的行为树。
    filename = dir_root + "bt_composition_planner/level3_combine_rules.xml"
    tree = ET.parse(filename)
    root = tree.getroot()
    rules = root.findall("rule")
    bt = None
    status_info = None
    for rule in rules:
        sent_xml = rule.find("sent").text
        code = rule.find("code").text
        # 对比两个句子的相似度
        sent_xml_vector = get_vector(sent_xml)
        sent_user_vector = get_vector(sent)
        soccer = cosine_similarity(sent_xml_vector, sent_user_vector)
        if soccer > 0.8:
            namespace = {'bt_list': bt_list, 'bt_create': bt_create}
            exec(code, namespace)
            bt = namespace['bt']
            status_info = namespace['status_info']
            break
    if status_info == "SUCCESS":
        return bt, status_info
    # TODO: 2 所有规则都无法匹配，调用大模型，针对该句添加规则到配置文件 level3_combine_rules.xml 中
    else:
        # TODO: 2.1 调用大模型生成对应的正则表达式和代码
        prompt = get_level3_combine_prompt(bt_list, sent)
        result_xml = llm.get_completion(prompt)
        flag = False
        for i in range(5):
            root = ET.fromstring(result_xml)[0]
            pattern = root.find("sent")
            match = re.search(pattern.text, sent, re.IGNORECASE)
            if not match:
                continue
            code = root.find("code")
            namespace = {'bt_list': bt_list, 'bt_create': bt_create}
            exec(code.text, namespace)
            bt = namespace['bt']
            status_info = namespace['status_info']
            if bt is not None and status_info == "SUCCESS":
                flag = True
                break
        # TODO: 2.2 如果正确匹配和生成行为树，则将这个规则保存到 xml 文件中
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
            with open(filename, 'w') as file:
                file.writelines(lines)
        else:
            return None, "ERROR: The behavior tree cannot be generated correctly, \
            please give a more detailed behavior tree! '" + sent + "'"
