import py_trees
import random


class Condition1(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(Condition1, self).__init__(name)

    def update(self):
        if is_condition_met():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


class Condition2(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(Condition2, self).__init__(name)

    def update(self):
        if is_condition_met():
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


def is_condition_met():
    # 在这里编写检查条件的代码
    print("检查移动前方是否有障碍物")
    random_number = random.uniform(0, 1)
    if (random_number < 0.5):
        return False
    return True
