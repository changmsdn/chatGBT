import py_trees
from py_trees import common


class grab_package(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(grab_package, self).__init__(name)

    def update(self) -> common.Status:
        print("grab_package")
        return py_trees.common.Status.SUCCESS


class route_plan(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(route_plan, self).__init__(name)

    def update(self) -> common.Status:
        print("route_plan")
        return py_trees.common.Status.SUCCESS


class moving_package(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(moving_package, self).__init__(name)

    def update(self) -> common.Status:
        print("moving_package")
        return py_trees.common.Status.SUCCESS


class place_package(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(place_package, self).__init__(name)

    def update(self) -> common.Status:
        print("place_package")
        return py_trees.common.Status.SUCCESS


class interrupt_operation(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(interrupt_operation, self).__init__(name)

    def update(self) -> common.Status:
        print("interrupt_operation")
        return py_trees.common.Status.SUCCESS


class notification_exception(py_trees.behaviour.Behaviour):
    def __init__(self, name: str):
        super(notification_exception, self).__init__(name)

    def update(self) -> common.Status:
        print("notification_exception")
        return py_trees.common.Status.SUCCESS

