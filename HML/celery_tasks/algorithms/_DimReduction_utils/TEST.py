from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
from celery_tasks.algorithms._DimReduction_utils import Test2
from celery_tasks.algorithms._DimReduction_utils.Test2 import f
from multiprocessing import Process, Pipe


if __name__ == '__main__':
    conn_1, conn_2 = Pipe()  # 生成管道的两边，分别传给两个进程
    p = Process(target=f, args=(conn_1,))
    p.start()
    print("Conn_2: ", conn_2.recv())
    print("Conn_2: ", conn_2.recv())
    conn_2.send("Data_1 from Conn_2")
    p.join()
    print("主")