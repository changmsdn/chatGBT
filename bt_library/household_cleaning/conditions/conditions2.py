import py_trees
import random


class clean_area_detection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(clean_area_detection, self).__init__(name)

    def update(self):
        if clean_area_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def clean_area_detection_impl():
    # 在这里编写检查条件的代码
    print("clean_area_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class cleaning_tool_detection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(cleaning_tool_detection, self).__init__(name)

    def update(self):
        if cleaning_tool_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def cleaning_tool_detection_impl():
    # 在这里编写检查条件的代码
    print("cleaning_tool_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class cleanliness(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(cleanliness, self).__init__(name)

    def update(self):
        if cleanliness_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def cleanliness_impl():
    # 在这里编写检查条件的代码
    print("cleanliness_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class envs_safety(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(envs_safety, self).__init__(name)

    def update(self):
        if envs_safety_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def envs_safety_impl():
    # 在这里编写检查条件的代码
    print("envs_safety_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True
