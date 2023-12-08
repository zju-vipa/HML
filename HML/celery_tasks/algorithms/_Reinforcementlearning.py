import pandas as pd
import numpy as np
import os
import sys
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
sys.path.append(ABSPATH)
#print(sys.path)
from  _Reinforcementlearning_utils.adjustflow import train as HML_RL
from  _Reinforcementlearning_utils.adjustflow import test as HML_RL_test
def algorithm_HML_RL_train(learner_id):
    HML_RL.main(flag='train',learner_id=learner_id, mode='human')
    
def algorithm_HML_RL_train_ML(learner_id):
    HML_RL.main(flag='train',learner_id=learner_id, mode='vanilla')
    
def algorithm_HML_RL_test(learner_id):
    HML_RL_test.main(flag='test',learner_id=learner_id, mode='human')
def algorithm_HML_RL_test_ML(learner_id):
    HML_RL_test.main(flag='test',learner_id=learner_id, mode='vanilla')
# if __name__ == '__main__':
#     algorithm_HML_RL_train()
