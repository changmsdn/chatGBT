import py_trees
from py_trees import common


class grab_parts(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(grab_parts, self).__init__(name)

    def update(self) -> common.Status:
        print("grab_parts")
        return py_trees.common.Status.SUCCESS


class positioning_parts(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(positioning_parts, self).__init__(name)

    def update(self) -> common.Status:
        print("positioning_parts")
        return py_trees.common.Status.SUCCESS


class assembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(assembly, self).__init__(name)

    def update(self) -> common.Status:
        print("assembly")
        return py_trees.common.Status.SUCCESS


class check_assembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(check_assembly, self).__init__(name)

    def update(self) -> common.Status:
        print("check_assembly")
        return py_trees.common.Status.SUCCESS


class interrupt_assembly(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(interrupt_assembly, self).__init__(name)

    def update(self) -> common.Status:
        print("interrupt_assembly")
        return py_trees.common.Status.SUCCESS


class request_help(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(request_help, self).__init__(name)

    def update(self) -> common.Status:
        print("request_help")
        return py_trees.common.Status.SUCCESS

