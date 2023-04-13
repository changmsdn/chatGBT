import xml.etree.ElementTree as ET

#  返回整个树
tree = ET.parse("test.xml")
root = tree.getroot()
print(root)

# 返回整个树的根节点
data = open("test.xml").read()
root = ET.fromstring(data)

for element in root.iter():
    print(element.get("name"))
