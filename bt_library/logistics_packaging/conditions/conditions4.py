import py_trees
import random


class package_detection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(package_detection, self).__init__(name)

    def update(self):
        if package_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def package_detection_impl():
    # 在这里编写检查条件的代码
    print("package_detection_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class package_type(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(package_type, self).__init__(name)

    def update(self):
        if package_type_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def package_type_impl():
    # 在这里编写检查条件的代码
    print("package_type_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class target_location(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(target_location, self).__init__(name)

    def update(self):
        if target_location_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def target_location_impl():
    # 在这里编写检查条件的代码
    print("target_location_impl")
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