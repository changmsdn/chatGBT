import py_trees
import random


class food_preparation(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(food_preparation, self).__init__(name)

    def update(self):
        if food_preparation_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def food_preparation_impl():
    # 在这里编写检查条件的代码
    print("food_preparation_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class cooking_utensils(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(cooking_utensils, self).__init__(name)

    def update(self):
        if cooking_utensils_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def cooking_utensils_impl():
    # 在这里编写检查条件的代码
    print("cooking_utensils_impl")
    random_number = random.uniform(0, 1)
    if random_number < 0.5:
        return False
    return True


class step_complete_detection(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(step_complete_detection, self).__init__(name)

    def update(self):
        if step_complete_detection_impl():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def step_complete_detection_impl():
    # 在这里编写检查条件的代码
    print("step_complete_detection_impl")
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
