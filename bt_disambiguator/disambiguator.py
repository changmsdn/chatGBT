def level1_bt_desc_error(sent):
    return "没有成功识别描述到行为树的映射！'…' 请更加详细些。详见使用说明！"


def level2_process_desc_error(condition):
    return "没有成功识别 ‘" + condition + "’ 到行为树的映射! '…' 请更加详细些。详见使用说明！"


def level3_task_desc_error(task_desc):
    return "现在还没有学习到 ‘ " + task_desc + " ’ 任务的实现! '…' 请更加详细些。详见使用说明！"


# 指代不明，比如 “创建一个顺序节点，孩子节点为顺序节点和选择节点。顺序节点执行Action1。”
#               前面有两个顺序节点，不知道接在哪个的下面。
def bt_desc_referential_error(text):
    return "请问你说的 ‘ " + text + " ’ 是前面提到的哪一个呢？"


# 行为树有些节点必须要带参数，比如 “执行grab任务，参数是 手机”
def bt_desc_no_param_error(text):
    return "对 ‘ " + text + " ’ 描述中缺少相应的参数。"
