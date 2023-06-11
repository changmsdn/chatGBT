import py_trees
from py_trees import common


class bypass(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(bypass, self).__init__(name)

    def update(self) -> common.Status:
        print("bypass")
        return py_trees.common.Status.SUCCESS


class charging(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(charging, self).__init__(name)

    def update(self) -> common.Status:
        print("charging")
        return py_trees.common.Status.SUCCESS


class drop(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(drop, self).__init__(name)

    def update(self) -> common.Status:
        print("drop")
        return py_trees.common.Status.SUCCESS


class grab(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(grab, self).__init__(name)

    def update(self) -> common.Status:
        print("grab")
        return py_trees.common.Status.SUCCESS


class move_back(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(move_back, self).__init__(name)

    def update(self) -> common.Status:
        print("move_back")
        return py_trees.common.Status.SUCCESS


class move_forward(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(move_forward, self).__init__(name)

    def update(self) -> common.Status:
        print("move_forward")
        return py_trees.common.Status.SUCCESS


class move_left(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(move_left, self).__init__(name)

    def update(self) -> common.Status:
        print("move_left")
        return py_trees.common.Status.SUCCESS


class move_right(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(move_right, self).__init__(name)

    def update(self) -> common.Status:
        print("move_right")
        return py_trees.common.Status.SUCCESS


class rest(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(rest, self).__init__(name)

    def update(self) -> common.Status:
        print("rest")
        return py_trees.common.Status.SUCCESS


class rotate(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(rotate, self).__init__(name)

    def update(self) -> common.Status:
        print("rotate")
        return py_trees.common.Status.SUCCESS


class scanning(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(scanning, self).__init__(name)

    def update(self) -> common.Status:
        print("scanning")
        return py_trees.common.Status.SUCCESS
