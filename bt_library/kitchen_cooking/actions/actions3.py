import py_trees
from py_trees import common


class prepare_food(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(prepare_food, self).__init__(name)

    def update(self) -> common.Status:
        print("prepare_food")
        return py_trees.common.Status.SUCCESS


class use_cooking_tools(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(use_cooking_tools, self).__init__(name)

    def update(self) -> common.Status:
        print("use_cooking_tools")
        return py_trees.common.Status.SUCCESS


class execution_steps(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(execution_steps, self).__init__(name)

    def update(self) -> common.Status:
        print("execution_steps")
        return py_trees.common.Status.SUCCESS


class finish_cooking(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(finish_cooking, self).__init__(name)

    def update(self) -> common.Status:
        print("finish_cooking")
        return py_trees.common.Status.SUCCESS


class interrupt_operation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(interrupt_operation, self).__init__(name)

    def update(self) -> common.Status:
        print("interrupt_operation")
        return py_trees.common.Status.SUCCESS


class request_intervention(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(request_intervention, self).__init__(name)

    def update(self) -> common.Status:
        print("request_intervention")
        return py_trees.common.Status.SUCCESS

