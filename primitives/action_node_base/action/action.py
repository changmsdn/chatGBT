import py_trees
from py_trees import common


class Action1(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action1, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS


class Action2(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action2, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS


class Action3(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action3, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS


class Action4(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action4, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS


class Action5(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action5, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS


class Action6(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(Action6, self).__init__(name)

    def update(self) -> common.Status:
        # action1任务逻辑
        print("我实现了Action1")
        return py_trees.common.Status.SUCCESS
