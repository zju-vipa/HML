import pandas as pd
import numpy as np
import os
import sys
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
sys.path.append(ABSPATH)
#print(sys.path)
from  _Reinforcementlearning_utils.section_adjust import train as HML_RL
def algorithm_HML_RL_train():
    HML_RL.main()
def algorithm_HML_RL_test(model):
    HML_RL.main(model)
if __name__ == '__main__':
    algorithm_HML_RL_train()
