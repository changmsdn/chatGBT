import py_trees
from py_trees import common


class navigate_to_area(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(navigate_to_area, self).__init__(name)

    def update(self) -> common.Status:
        print("navigate_to_area")
        return py_trees.common.Status.SUCCESS


class use_cleaning_tools(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(use_cleaning_tools, self).__init__(name)

    def update(self) -> common.Status:
        print("use_cleaning_tools")
        return py_trees.common.Status.SUCCESS


class clean_area(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(clean_area, self).__init__(name)

    def update(self) -> common.Status:
        print("clean_area")
        return py_trees.common.Status.SUCCESS


class check_cleanliness(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(check_cleanliness, self).__init__(name)

    def update(self) -> common.Status:
        print("check_cleanliness")
        return py_trees.common.Status.SUCCESS


class interrupt_operation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(interrupt_operation, self).__init__(name)

    def update(self) -> common.Status:
        print("interrupt_operation")
        return py_trees.common.Status.SUCCESS


class request_help(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(request_help, self).__init__(name)

    def update(self) -> common.Status:
        print("request_help")
        return py_trees.common.Status.SUCCESS

