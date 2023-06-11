from bt_instruction2bt_mapper.bt_tools import *
from bt_disambiguator.disambiguator import *
from bt_language_parser.parser import *
import llm.llm as llm


def get_level3_bt_from_bt_desc_prompt(bt_desc):
    prompt = f"""
According to the intent described in the quotes after "desc: ", \
one of the behavior tree nodes available below is selected as the answer to generate.

The available behavior tree nodes are:
{get_bts_info_prompt()}

Example:
desc: "ask for help"
request_help
desc: "是否存在危险物品或障碍物"
envs_safety


Require:
- only print behavior tree node names
- If no behavior tree node matching this condition is found in the intent, return "None"

desc: "{bt_desc}"
    """
    return prompt


def get_level3_generate_fine_tune_prompt(step, result_xml, abilities, sent):
    prompt = f"""
The answer you generate is:
{result_xml}

Among them, "{step}" cannot correctly extract the operation corresponding to the specific robot capability.
The robot's capabilities are:
{abilities}

Please regenerate the result.

Require:
- The steps need to be designed according to the capabilities of the robot
- Only generate xml structure, do not print redundant information.

"Control Instruction: "{sent}"
"""
    return prompt


def get_level3_generate_prompt(sent, area, abilities):
    prompt = f"""
Now there is a robot in the {area} field that responds by accepting instructions. \
Next, according to the given "Control Instructions", \
give the specific steps that the robot should perform to perform this task, \
and generate the results in xml format as follows:

Example:
sent: Execute the task: make a beef fried noodles
<rule>
     <sent>Execute the task: make a beef fried noodles</sent>
     <steps>
         <step>Check if you have the required cooking tools</step>
         <step>Check for dangerous objects or obstacles</step>
         <step>Check if there are prepared ingredients</step>
         <step>Check if the previous step has been completed</step>
         <step>Process and prepare the required ingredients</step>
         <step>Follow the cooking steps</step>
         <step>Complete the whole cooking process</step>
         <step>Interrupt operation when encountering obstacles or dangerous situations</step>
         <step>Get human operator intervention and guidance</step>
         <step>Use cooking tools for cooking operation</step>
     </steps>
</rule>
   
The robot has the ability to:
{abilities}

Require:
- The steps need to be designed according to the capabilities of the robot
- Only generate xml structure, do not print redundant information.

"Control Instruction: "{sent}"
    """
    return prompt


def create_level3_bt_list(sent):
    """
    :param sent: "任务"描述级语言
    :return: 行为树节点列表
    """
    # TODO: 1 读取 level3_generator_rules.xml。获取sent句子，对比相似度。如果符合则使用该规则。
    filename = dir_root + "bt_builder/level3_generator_rules.xml"
    tree = ET.parse(filename)
    root = tree.getroot()
    rules = root.findall("rule")
    bt_list = []
    bt_desc_list = []
    status_info = None
    for rule in rules:
        # 对比句子
        sent_from_xml = rule.find("sent").text
        if sent_from_xml == sent:
            steps = rule.find("steps")
            for step in steps:
                bt_desc_list.append(step.text)
            status_info = "SUCCESS"
        # 对比相似度
        sent_from_xml_vector = get_vector(sent_from_xml)
        sent_user_vector = get_vector(sent)
        soccer = cosine_similarity(sent_from_xml_vector, sent_user_vector)
        if soccer > 0.9:
            steps = rule.find("steps")
            for step in steps:
                bt_desc_list.append(step.text)
            status_info = "SUCCESS"
    # TODO: 2 根据 bt_desc_list 得到对应的 bt节点，如果匹配不到，则调用歧义消解模块
    if status_info == "SUCCESS":
        for bt_desc in bt_desc_list:
            node_name, node_type = find_bt(bt_desc)
            if node_name is not None and node_type != -1:
                bt_info = {"name": node_name, "type": node_type}
                bt_list.append(bt_info)
            else:
                prompt = get_level3_bt_from_bt_desc_prompt()
                result = llm.get_completion(prompt)
                if "None" not in result:
                    bt_list.append(result)
                    add_synonyms_to_bt_library(bt_desc)
                    pass
                else:
                    return None, "ERROR: There is no corresponding behavior tree node, \
                and further decomposition may be required. '" + bt_desc + "' !!"
        return bt_list, "SUCCESS"
    # TODO: 3 所有已有规则都不匹配。调用大模型，生成新的规则，并且保存到 level2_generator_rules.xml中
    else:
        # TODO: 3.1 获取 级别3语言的正则表达式提示词，然后调用 ChatGPT 生成正则表达式
        area = get_robot_area()
        abilities = get_bts_abilities_prompt()
        prompt = get_level3_generate_prompt(sent, area, abilities)
        print(prompt)
        result_xml = llm.get_completion(prompt, temperature=0, model="gpt-3.5-turbo")
        flag = True
        for i in range(5):
            # TODO: 3.2 进行 bt_list 生成的检验，防止 llm 生成的答案不尽如人意
            root = ET.fromstring(result_xml)[1]
            for step in root.findall("step"):
                node_name, node_type = find_bt(step.text)
                if node_name is not None and node_type != -1:
                    bt_info = {"name": node_name, "type": node_type}
                    bt_list.append(bt_info)
                else:
                    # TODO: 3.3 llm 提示词指令进行微调，重新生成从句子中提取的 xml 意图模板
                    flag = False
                    prompt = get_level3_generate_fine_tune_prompt(step, result_xml, abilities, sent)
                    print(prompt)
                    result_xml = llm.get_completion(prompt, temperature=0, model="gpt-3.5-turbo")
                    break
            if flag is True:
                break
        # TODO: 3.4 如果成功解析了，将该 xml 添加到文件中
        if flag is True:
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
            return bt_list, "SUCCESS"
        else:
            return None, "Error: llm cannot parse your command, \
            please enter a more precise command. '" + sent + "'"
