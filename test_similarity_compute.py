import spacy
import numpy as np
from bt_language_parser.parser import *

"""
异常记录：
【the same time】【the】：0.8078883466564888
【at the same time】【the】：0.6753267195106382
"""

if __name__ == '__main__':
    # 读取一个有词向量的较大流程
    nlp = spacy.load("en_core_web_md")
    # 比较两个文档
    # doc1 = nlp("the same time")
    doc1 = nlp("at the same time")
    v1 = doc1.vector
    # doc2 = nlp("the")
    doc2 = nlp("the same time")
    v2 = doc2.vector
    print(doc1.similarity(doc2))
    so = cosine_similarity(v1, v2)
    print(so)
