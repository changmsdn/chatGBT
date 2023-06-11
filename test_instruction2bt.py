from bt_instruction2bt_mapper.instruction2bt import *


if __name__ == '__main__':
    # level3: task_desc
    # text = "执行任务，get_me_something"    # success
    # text = "执行任务帮我拿点东西"    # 现在还没有学习到 ‘ 帮我拿点东西 ’ 任务的实现
    # primitive, bt_desc = primitive_generate_task(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(primitive))
    # else:
    #     print(bt_desc)

    # level2: process_desc
    # text = "如果前面有障碍物，就绕行。"    # 成功
    # text = "如果明天不下雨，就去公园玩。"  # 没有成功识别‘明天不下雨’到行为树的映射
    # text = "如果前面有人，就绕行。"       # 没有成功识别‘前面有人’到行为树的映射
    # text = "如果前面有障碍物，就飞过去。"   # 没有成功识别‘飞过去’到行为树的映射
    # primitive, bt_desc = primitive_generate_pattern(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(primitive))
    # else:
    #     print(bt_desc)

    # text = "首先检查环境中是否有障碍物，接着前进到指定位置，最后抓取它。" # success
    # text = "首先，检查环境中是否有障碍物，最后抓取它。"  # success
    # text = "首先，扫描环境，然后再检查环境中是否有障碍物，最后找到手机。"  # 没有成功识别 ‘ 找到手机 ’ 到行为树的映射
    # primitive, bt_desc = primitive_generate_pattern(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(primitive))
    # else:
    #     print(bt_desc)

    # text = "检查环境中是否有障碍物，以及前进到指定位置，或者抓取它。"  # success
    # text = "检查环境中是否有障碍物，以及前进到指定位置，并且学习一下。"  # 没有成功识别 ‘ 学习一下 ’ 到行为树的映射
    # text = "首先，检查环境中是否有障碍物，最后抓取它。"
    # primitive, bt_desc = primitive_generate_pattern(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(primitive))
    # else:
    #     print(bt_desc)

    # level1: bt_desc
    """
        ------------------------- 第一轮 ---------------------------------
        有障碍物就避障
    """
    # text = "执行一个sequence节点，然后添加子节点grab_package, moving_package。"

    # text = "Execute a sequence node with child nodes grab_package, moving_package, and place_package."
    # text = "Add child nodes moving_package, target_location, and grab_package to the sequence node."

    text = "Detect the package type and grab it, then place it at the target location."
    # text = "Grab the package and mail it to the target location at the same time."

    bt, bt_desc = instruction_to_bt(text)
    if bt_desc == "SUCCESS":
        print(py_trees.display.unicode_tree(bt))  # 打印行为树
        # 暂存
        save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
        py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
        # 重用
        print("执行结束，重用它")
        task_reuse_name = "avoid_obstacle"

        dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
        if not os.path.exists(dir_save_images):
            os.makedirs(dir_save_images)
        save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
        py_trees.display.render_dot_tree(bt, name=task_reuse_name,
                                         target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    else:
        print(bt_desc)

    """
        ------------------------- 第二轮 ---------------------------------
        没电就充电
    """
    # text = "执行一个selector节点，子节点为battery_check和charging。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "check_and_charging"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #     ------------------------- 第三轮 ---------------------------------
    #     探索
    # """
    # text = "执行一个parallel，子节点为selector和scanning"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    # else:
    #     print(bt_desc)
    #
    # text = "selector子节点执行move_forward和avoid_obstacle"
    # bt, bt_desc = text_to_bt(text, bt)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "explore"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #     ------------------------- 第四轮 ---------------------------------
    #     寻找东西并拿到它
    # """
    # text = "执行一个sequence任务，子节点为selector、sequence。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    # else:
    #     print(bt_desc)
    #
    # text = "sequence的孩子reachable、grab。selector的子节点为visible和explore。"
    # bt, bt_desc = text_to_bt(text, bt)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "find_and_grab"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
    #
    # """
    #         ------------------------- 第五轮 ---------------------------------
    #         帮我拿XX过来
    #     """
    # text = "执行一个sequence任务，子节点为check_and_charging、find_and_grab、explore。"
    # bt, bt_desc = text_to_bt(text)
    # if bt_desc == "SUCCESS":
    #     print(py_trees.display.unicode_tree(bt))  # 打印行为树
    #     # 暂存
    #     save_bt2xml(bt, "temp", dir_tasks_reuse + "temp/temp.xml")
    #     py_trees.display.render_dot_tree(bt, name="temp", target_directory=dir_tasks_reuse + "temp")
    #     # 重用
    #     print("执行结束，重用它")
    #     task_reuse_name = "get_me_something"  # 和基础charging重名，之后会覆盖它
    #     dir_save_images = dir_tasks_reuse + "images/" + task_reuse_name
    #     if not os.path.exists(dir_save_images):
    #         os.makedirs(dir_save_images)
    #     save_bt2xml(bt, task_reuse_name, dir_tasks_reuse + task_reuse_name + ".xml")
    #     py_trees.display.render_dot_tree(bt, name=task_reuse_name,
    #                                      target_directory=dir_tasks_reuse + "images/" + task_reuse_name)
    # else:
    #     print(bt_desc)
