import subprocess
import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
"""
nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_core_web_md")
nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("zh_core_web_sm")
nlp = spacy.load("zh_core_web_md")
nlp = spacy.load("zh_core_web_lg")
"""
# 运行Shell命令
command = 'python -m spacy download en_core_web_lg'
# command = 'python -m spacy download zh_core_web_sm'
result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')

# 打印命令输出
print(result.stdout)
