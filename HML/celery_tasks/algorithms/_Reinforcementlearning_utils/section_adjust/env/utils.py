import pickle


def save_variable(v, filename):
    """
    保存 python 变量
    :param v: 变量
    :param filename: 文件名
    """
    f = open(filename, 'wb')
    pickle.dump(v, f)
    f.close()


def load_variable(filename):
    """
    读取 python 变量
    :param filename: 文件名
    :return v: 变量
    """
    f = open(filename, 'rb')
    v = pickle.load(f)
    f.close()
    return v