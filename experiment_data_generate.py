from llm.llm import *


def get_prompt_zh(task, all_infos):
    prompts = f"""

        According to the specific robot, generate a specific behavior tree xml through natural language:

        The field of application of this robot is '{task}'.
        The specific robot uses the behavior tree engine as the underlying control architecture.
        The 'specific available behavior tree node' information is as follows:

        {all_infos}

        Explanations:
        - In 'specific available behavior tree node' information, the reuse task needs \
        to be generated through reuse after continuous interaction, so it may be empty, \
        so don't worry about it.
        - In the natural language generation behavior tree, the natural language is mapped \
        to the behavior tree node, and the mapping must be performed \
        by using the above available behavior tree node names or synonyms as trigger words.
        - Natural language description is divided into three levels: 
        level 1 language describes the specific structure of behavior tree nodes, \
        which requires a certain degree of behavior tree expertise; 
        For example: Execute a selector node, then add child nodes correct_positioning \
        and envs_safety, and a parallel node that contains grab_parts and request_help as child nodes.
        level 2 describes the specific process of task execution, and the process details \
        need to be implemented in the specific operation process of the robot.\
        Compared with level 1, level 2 does not need to describe behavior tree nodes;
        For example: First check whether the workpiece is placed correctly, \
        confirm that the environment is safe and whether the parts in the environment \
        are complete, and then ask for assistance and get the parts at the same time.
        level 3 Directly describe the user's needs, compared with Level 2, \
        there is no need to describe the specific operation process.
        For example: Execute tasks: Check that the component status is correct.

        Please generate 12 pieces of xml data. Contains three tags of 'level', 'desc' and 'bt', \
        and each data is represented by an instruction tag

        Examples:
        <instruction>
            <level>1</level>
            <desc>执行一个selector节点，然后添加子节点correct_positioning和envs_safety</desc>
            <bt>
                <selector name='selector' type="controller">
                    <correct_positioning name='correct_positioning' type="action"/>
                    <envs_safety name='envs_safety' type="condition"/>
                </selector>
            </bt>
        </instruction>
        <instruction>
            <level>2</level>
            <desc>拿起必要的零件并在必要时寻求帮助。</desc>
            <bt>
                <selector name='selector' type="controller">
                    <grab_parts name='grab_parts' type="action"/>
                    <request_help name='request_help' type="action"/>
                </selector>
            </bt>
        </instruction>
        <instruction>
            <level>3</level>
            <desc>执行任务：安全组装零件。</desc>
            <bt>
                <selector name='assembly' type="controller">
                    <envs_safety name='envs_safety' type="condition"/>
                    <sequence name='sequence' type="controller">
                        <correct_positioning name='correct_positioning' type="action"/>
                        <assembly name='assembly' type="controller">
                            <assembly_parts name='assembly_parts' type="action"/>
                        </assembly>
                    </sequence>
                </selector>
            </bt>
        </instruction>

        Requirements:
        - In the generated xml, there are 8 items of level 1, 3 items of level 2, and 1 item of level 3.
        - The 'desc' use Chinese.
        - The "level 1"'s "desc" must use the exact same name as the node available above.\
        For example: "Execute a selector node, and then add child nodes grab_parts and positioning_parts."\
        Include trigger words 'generate node','create node' or 'add child node' etc.
        - The "level 2"'s "desc" cannot contain level 1 trigger words 'add child' etc.
        For example: "Grab the required parts, position them correctly, and then assemble the parts."
        - The "level 3"'s "desc" do not express the task process, only express the purpose requirements.\
        For example, "Execution task: Get me a cell phone." "Execution task: Go and clean up the kitchen." 
        Include trigger words 'execution task:','perform tasks:' or 'task execution:' etc.
        - The number of words for 'desc' is randomized from 1 word to 20 words.
        - The tag in 'bt' must have exactly the same name as the 'specific available behavior tree node' above.
        - Do not print serial number.
        - The value of bt is to construct a behavior tree of consistent intent logic based on "desc". 
            """
    return prompts


def get_prompt_en(task, all_infos):
    prompts = f"""

    According to the specific robot, generate a specific behavior tree xml through natural language:

    The field of application of this robot is '{task}'.
    The specific robot uses the behavior tree engine as the underlying control architecture.
    The 'specific available behavior tree node' information is as follows:

    {all_infos}

    Explanations:
    - In 'specific available behavior tree node' information, the reuse task needs \
    to be generated through reuse after continuous interaction, so it may be empty, \
    so don't worry about it.
    - In the natural language generation behavior tree, the natural language is mapped \
    to the behavior tree node, and the mapping must be performed \
    by using the above available behavior tree node names or synonyms as trigger words.
    - Natural language description is divided into three levels: 
    level 1 language describes the specific structure of behavior tree nodes, \
    which requires a certain degree of behavior tree expertise; 
    For example: Execute a selector node, then add child nodes correct_positioning \
    and envs_safety, and a parallel node that contains grab_parts and request_help as child nodes.
    level 2 describes the specific process of task execution, and the process details \
    need to be implemented in the specific operation process of the robot.\
    Compared with level 1, level 2 does not need to describe behavior tree nodes;
    For example: First check whether the workpiece is placed correctly, \
    confirm that the environment is safe and whether the parts in the environment \
    are complete, and then ask for assistance and get the parts at the same time.
    level 3 Directly describe the user's needs, compared with Level 2, \
    there is no need to describe the specific operation process.
    For example: Execute tasks: Check that the component status is correct.

    Please generate 12 pieces of xml data. Contains three tags of 'level', 'desc' and 'bt', \
    and each data is represented by an instruction tag

    Examples:
    <instruction>
        <level>1</level>
        <desc>Execute a selector node, then add child nodes correct_positioning and envs_safety</desc>
        <bt>
            <selector name='selector' type="controller">
                <correct_positioning name='correct_positioning' type="action"/>
                <envs_safety name='envs_safety' type="condition"/>
            </selector>
        </bt>
    </instruction>
    <instruction>
        <level>2</level>
        <desc>Grab the necessary parts and request help when necessary.</desc>
        <bt>
            <selector name='selector' type="controller">
                <grab_parts name='grab_parts' type="action"/>
                <request_help name='request_help' type="action"/>
            </selector>
        </bt>
    </instruction>
    <instruction>
        <level>3</level>
        <desc>Execution task: Assemble the parts safely.</desc>
        <bt>
            <selector name='assembly' type="controller">
                <envs_safety name='envs_safety' type="condition"/>
                <sequence name='sequence' type="controller">
                    <correct_positioning name='correct_positioning' type="action"/>
                    <assembly name='assembly' type="controller">
                        <assembly_parts name='assembly_parts' type="action"/>
                    </assembly>
                </sequence>
            </selector>
        </bt>
    </instruction>

    Requirements:
    - In the generated xml, there are 8 items of level 1, 3 items of level 2, and 1 item of level 3.
    - The "level 1"'s "desc" must use the exact same name as the node available above.\
    For example: "Execute a selector node, and then add child nodes grab_parts and positioning_parts."\
    Include trigger words 'generate node','create node' or 'add child node' etc.
    - The "level 2"'s "desc" cannot contain level 1 trigger words 'add child' etc.
    For example: "Grab the required parts, position them correctly, and then assemble the parts."
    - The "level 3"'s "desc" do not express the task process, only express the purpose requirements.\
    For example, "Execution task: Get me a cell phone." "Execution task: Go and clean up the kitchen." 
    Include trigger words 'execution task:','perform tasks:' or 'task execution:' etc.
    - The number of words for 'desc' is randomized from 1 word to 20 words.
    - The tag in 'bt' must have exactly the same name as the 'specific available behavior tree node' above.
    - Do not print serial number.
    - The value of bt is to construct a behavior tree of consistent intent logic based on "desc". 
        """
    return prompts


if __name__ == '__main__':
    # 1 获取实体已知资源：机器人的行为能力，感知能力。所处的世界位置等。
    # task_area = "manufacturing_assembly"
    # task_area = "logistics_packaging"
    # task_area = "kitchen_cooking"
    task_area = "household_cleaning"
    all_info = get_bts_info_prompt()
    print(task_area)
    print(all_info)

    # 2 获得想要的提示词
    # 2.1 英文
    # prompt = get_prompt_en(task_area, all_info)
    # fo = open("experiment/dataset/manufacturing_assembly/dataset_en.xml", mode="a", encoding="utf-8")
    # fo = open("experiment/dataset/logistics_packaging/dataset_en.xml", mode="a", encoding="utf-8")
    # fo = open("experiment/dataset/kitchen_cooking/dataset_en.xml", mode="a", encoding="utf-8")
    # fo = open("experiment/dataset/household_cleaning/dataset_en.xml", mode="a", encoding="utf-8")

    # 2.2 中文
    prompt = get_prompt_zh(task_area, all_info)
    # fo = open("experiment/dataset/manufacturing_assembly/dataset_zh.xml", mode="a", encoding="utf-8")
    # fo = open("experiment/dataset/logistics_packaging/dataset_zh.xml", mode="a", encoding="utf-8")
    # fo = open("experiment/dataset/kitchen_cooking/dataset_zh.xml", mode="a", encoding="utf-8")
    fo = open("dataset/household_cleaning/dataset_zh.xml", mode="a", encoding="utf-8")

    # 3 得到数据，并且写入到具体的文件
    fo.write("<root>\n")
    for i in range(50):
        # 1 通过 chat-gpt 获得数据
        response = get_completion(prompt, 0.95)
        # 2 将数据写入到examples中
        fo.write(response)
    fo.write("\n</root>")
    fo.close()
