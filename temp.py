class TreeNode:
    def __init__(self, val):
        self.val = val
        self.children = []


def traverse(root):
    if root is None:
        return

    # 使用栈进行DFS遍历，初始栈中只包含根节点
    stack = [root]
    while stack:
        # 弹出栈顶节点，并将其子节点倒序加入栈中
        node = stack.pop()
        for i in range(len(node.children) - 1, -1, -1):
            stack.append(node.children[i])

        # 遍历当前节点
        visit(node)


def visit(node):
    print(node.val)


# 创建测试用例
root = TreeNode(1)
node2 = TreeNode(2)
node3 = TreeNode(3)
node4 = TreeNode(4)
node5 = TreeNode(5)
node6 = TreeNode(6)
node7 = TreeNode(7)
root.children = [node2, node3]
node2.children = [node4, node5]
node3.children = [node6, node7]

# 从下到上、从右到左遍历多叉树
traverse(root)
