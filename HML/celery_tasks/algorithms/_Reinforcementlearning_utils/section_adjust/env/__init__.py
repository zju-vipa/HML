import os

# 代码存储绝对路径
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
print(ABSPATH)
#sys.path.append(ABSPATH)
code_path = ABSPATH+"/../data"
assert code_path, "需要定义代码存储绝对路径"

# 数据存储绝对路径
ROOT_PATH = os.path.join(code_path)

