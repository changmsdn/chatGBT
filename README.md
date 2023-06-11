# ChatGBT
使用自然语言生成行为树的引擎

# 1 安装需要

## 1.1 第三方项目依赖下载
### 1 py_trees 
- 注意pydot要使用conda的下载
### 2 ppasr
- 根据requirement.txt来下载，不要使用setup.py
- 还有很多依赖包，如解码，itn，pyni等都需要额外安装。可以运行时不断排错安装即可
### 3 spacy
- 注意使用shell代理，然后下载相关模型

## 1.2 chat-gbt 项目依赖下载
- 根据requirement.txt来下载

# 2 功能实现
## 1 已完成
1 通过每一句指令生成一个行为树。

2 人机交互界面

3 数据集测试

## 2 待优化
1 combine_bt_nodes 和 combine_between_bts 的优化

2 llm prompt的优化

## 3 未来
1 task_reuse 如何抽象存储 以及 可重用行为树本身的优化。

2 如何更好的利用 llm

3 基于意图识别 rasa
