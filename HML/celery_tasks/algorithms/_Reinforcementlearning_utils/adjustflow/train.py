import argparse
import os
import time
import sys
import torch
import numpy
import gym
from datetime import datetime

from dao import LearnerDao
from model import db, Learner
learnerDao = LearnerDao(db)
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
# print('ABSPATH:', ABSPATH)
sys.path.append(ABSPATH)
import matplotlib.pyplot as plt

from askrl.stable_baselines3 import AskPPO, PPO
from askrl.stable_baselines3.common.monitor import Monitor
from askrl.stable_baselines3.common.utils import linear_schedule

from PSASPEnv_v2 import PSASPEnv
from PSASPEnv_v2 import copy_dirs

from flask import current_app

class AskAction(gym.Wrapper):
    def __init__(self, env):
        super(AskAction, self).__init__(env)
        self.action_space = gym.spaces.Discrete(n=self.action_space.n+1)


def get_env(args):
    env = PSASPEnv(args)
    env.seed(args.seed)
    env.reset()
			   
    env.action_space.seed(args.seed)
    env = Monitor(env)

    if args.mode == 'human':
        env = AskAction(env)

    return env


def get_model(env, args):
    model = None

    if args.mode == 'vanilla':
        if args.algo == 'ppo':
            model = PPO('MlpPolicy', env, learning_rate=linear_schedule(0.001), n_steps=256, batch_size=256, n_epochs=10,
                        gamma=0.99, gae_lambda=0.95, clip_range=linear_schedule(0.2), clip_range_vf=None, ent_coef=0.0,
                        vf_coef=0.5, max_grad_norm=0.5, target_kl=None, tensorboard_log=args.work_dir, create_eval_env=False,
                        policy_kwargs=None, verbose=1, seed=args.seed)
    if args.mode == 'human':
        if args.algo == 'ppo':
            model = AskPPO('MlpPolicy', env, learning_rate=linear_schedule(0.001), n_steps=256, batch_size=256, n_epochs=10,
                           gamma=0.99, gae_lambda=0.95, clip_range=linear_schedule(0.2), clip_range_vf=None, ent_coef=0.0,
                           vf_coef=0.5, max_grad_norm=0.5, target_kl=None, tensorboard_log=args.work_dir,
                           create_eval_env=False, policy_kwargs=None, verbose=1, seed=args.seed, human_policy=None)

    assert model, "model not exist"
    return model


def get_human_policy(learner_id):

    def human_policy(state, info, env):
        if info is None:
            info = env.get_action_info()
            action_idx = info['action_idx']
            for action in range(220):
                if action not in action_idx:
                    _, _, _, info = env.step(action)
                    break								
										   
        print("==== info ====")
        # print(info)
        
        #print("P:")
        
        import pandas as pd

        # result 为插入的list数据
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner_id)
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)
        file_name = 'action_pqvt'
        file_path = os.path.join(file_directory, file_name)
        # path = "action_pqvt.csv"
        #if(not os.path.exists(path)): os.makedirs(path)
        info = info[0]
        netDetailInfoColumns = {
          'v_pair': ['name', 'voltage', 'voltageLowerLimit', 'voltageHighLimit', 'voltageInfo'],
          # 'balance_pair': ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
          'line_pair': ['name', 'power'],
          'gen_pair': ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
          'sec_pair': ['name', 'power', 'powerLowerLimit', 'powerHighLimit', 'powerInfo'],
          'target_sec_pair': ['name', 'now', 'target'],
        }
        
        def map_func(x, item) :
          out={}
          for i in range(len(item)):
            out[item[i]]=x[i]
          return out
        
        for key, value in netDetailInfoColumns.items():
          nn = list(map(lambda x: map_func(x, value), info[key]))
          info[key]=list(nn)
          
        numpy.save(file_path, info)

        #action = input("Human Action:")
        #return action
        # learner = learnerService.queryLearnerById(learner_id)
        learner = learnerDao.queryLearnerById(learner_id)
        learner.action = -1
        # learnerService.updateLearner(learner)
        learnerDao.updateLearner(learner)
        current_app.logger.info("get human policy update action=-1")
        current_app.logger.info(learner.learner_name)
        # DB write  action = -1
        while (1==1):
            current_app.logger.info("get human policy while-loop")
            import time
            time.sleep(10)
            # learner = learnerService.queryLearnerById(learner_id)
            learner = learnerDao.queryLearnerById(learner_id)
            # 每次查询后更新一下，不然下次查询的结果就是这次的快照，而不会重新从数据库里读取
            learnerDao.updateLearner(learner)
            action = learner.action
            current_app.logger.info(action)
            if(action!=-1):
                current_app.logger.info("get human policy action!=-1")
                current_app.logger.info(learner.learner_name)
                current_app.logger.info(action)
                return action
        print("==== info ====")
    return human_policy


def train(args, learner_id):
    current_app.logger.info("RL train.train begin")
    env = get_env(args)
    model = get_model(env, args)
    current_app.logger.info(model)

    if args.mode == 'human':
        model.human_policy = get_human_policy(learner_id)

    model.learn(total_timesteps=args.total_timesteps, reset_num_timesteps=True)
    current_app.logger.info("RL train.train model.learn")
    model.save(os.path.join('rl_model_final'))


def main(flag = 'train', learner_id=None):
    current_app.logger.info("RL train.main begin")
    class Parser():
        def __init__(self):
            self.env_id = 'case300'
            self.mode = 'human'
            self.algo = 'ppo'
            self.total_timesteps = int(5e4)
            self.seeds = '[404]'
            self.info = 'reward_gen'
            self.gpu = '0'
            self.case_file = 'LF'
            self.data_dir = 'data'
            self.scence_file = 'scence.npy'
            self.is_training = True

    args = Parser()
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
    args.data_dir = os.path.join(ABSPATH,args.data_dir)
    seeds = list(map(int, args.seeds.strip('[]').split(',')))

    log_datetime = datetime.now()

    for i in range(len(seeds)):
        log_exp_name = args.env_id + '_' + args.mode + '_' + args.algo + '_' + args.info
        log_exp_name = log_exp_name + '_' + str(seeds[i])
        args.work_dir = os.path.join(ABSPATH, 'askrl', 'exp_v1', log_datetime.strftime('%Y-%m-%d-%H-%M-%S-') + log_exp_name)
        args.seed = seeds[i]
        
        if flag == 'train':
            copy_dirs(args.data_dir, args.work_dir)
            train(args, learner_id)


if __name__ == '__main__':
    main('train')



