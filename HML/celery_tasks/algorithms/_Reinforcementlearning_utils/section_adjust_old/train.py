import gym
import os
import sys

from dao import LearnerDao
from model import db, Learner
learnerDao = LearnerDao(db)
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
sys.path.append(ABSPATH)
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from askrl.stable_baselines3 import PPO, AskPPO, DQN
from askrl.stable_baselines3.common.monitor import Monitor
from askrl.stable_baselines3.common.utils import linear_schedule
from askrl.stable_baselines3.common.callbacks import CheckpointCallback
from askrl.stable_baselines3.common.evaluation import evaluate_policy
from env.transmission_section import TransmissionSectionEnv
from flask import current_app

class AskAction(gym.Wrapper):
    def __init__(self, env):
        super(AskAction, self).__init__(env)
        self.action_space = gym.spaces.Discrete(n=self.action_space.n+1)


def get_env(args):
    env = TransmissionSectionEnv(args)
    env.seed(args.seed)
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
                        vf_coef=0.5, max_grad_norm=0.5, target_kl=None, tensorboard_log=args.log_dir, create_eval_env=False,
                        policy_kwargs=None, verbose=1, seed=args.seed)
    if args.mode == 'human':
        if args.algo == 'ppo':
            model = AskPPO('MlpPolicy', env, learning_rate=linear_schedule(0.001), n_steps=256, batch_size=256, n_epochs=10,
                           gamma=0.99, gae_lambda=0.95, clip_range=linear_schedule(0.2), clip_range_vf=None, ent_coef=0.0,
                           vf_coef=0.5, max_grad_norm=0.5, target_kl=None, tensorboard_log=args.log_dir,
                           create_eval_env=False, policy_kwargs=None, verbose=1, seed=args.seed, human_policy=None,
                           use_baseline_ask=args.use_baseline_ask, ask_threshold=args.ask_threshold, use_ask_loss=True)

    assert model, "model not exist"
    return model


def get_human_policy(learner_id):
    # model_path = "askrl/exp_v1/2021-11-12_PSASP300_vanilla_ppo_reward_gen_404/18-41-07/rl_model_final.zip"
    # model = PPO.load(model_path)
    current_app.logger.info("get human policy begin")

    def human_policy(state):
        # action, _ = model.predict(state.cpu(), deterministic=True)
        state = state.cpu().numpy()

        #print("P:")
        P = (state[0::4])
        Q = (state[1::4])
        V = (state[2::4])
        Theta = (state[3::4])
        import pandas as pd

        # result 为插入的list数据
        file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner_id)
        if not os.path.exists(file_directory):
            os.mkdir(file_directory)
        file_name = 'action_pqvt.csv'
        file_path = os.path.join(file_directory, file_name)
        # path = "action_pqvt.csv"
        #if(not os.path.exists(path)): os.makedirs(path)
        test = pd.DataFrame({'P': P, 'Q': Q, "V": V, "Theta": Theta})
        test.to_csv(file_path)

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


    return human_policy


def train(args, learner_id):
    current_app.logger.info("RL train.train begin")
    env = get_env(args)
    model = get_model(env, args)
    current_app.logger.info(model)

    if args.use_baseline_ask != '':
        model.use_ask_loss = False

    if args.mode == 'human':
        model.human_policy = get_human_policy(learner_id)   #不用就改成none

    checkpoint_callback = CheckpointCallback(save_freq=5000, save_path=args.log_dir, name_prefix='rl_model')
    model.learn(total_timesteps=args.total_timesteps, callback=checkpoint_callback, reset_num_timesteps=True)
    current_app.logger.info("RL train.train model.learn")
    # model.learn(total_timesteps=args.total_timesteps, callback=checkpoint_callback, reset_num_timesteps=True)
    # print(args.log_dir)
    # model.save(os.path.join(args.log_dir, 'rl_model_final'))
    model.save(os.path.join('rl_model_final'))

def test(args):   # test时不会向人类提问
    current_app.logger.info("RL train.test begin")
    env = get_env(args)
    model_path = "rl_model_final.zip"
    if args.mode == 'vanilla':
        model = PPO.load(model_path)
    else:
        model = AskPPO.load(model_path)
        model.human_policy = None
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100, render=False, deterministic=False)
    print(env.action_count)
    print("seed {}: mean_reward: {:.1f}, std_reward: {:.1f}".format(args.seed, mean_reward, std_reward))

    #plt.figure()
    #plt.bar(np.arange(len(env.action_count)), env.action_count, width=0.8, bottom=2, color='r', alpha=0.8, edgecolor='k', linewidth=1)
    #plt.show()
    return mean_reward   # 以后可以考虑返回点别的东西。
def main(flag = 'train', learner_id=None):
    current_app.logger.info("RL train.main begin")
    class Parser():
        def __init__(self):
            self.env_id = 'case118'
            self.mode = 'human'
            # self.mode = 'vanilla'
            self.algo = 'ppo'
            self.total_timesteps = int(5e4)
            # self.total_timesteps = int(1e2)
            self.seeds = '[404]'
            self.exp = 'run'
            self.use_baseline_ask = ''
            self.ask_threshold = 0.6
            self.info = 'reward_gen'
            self.gpu = '0'
            self.work_dir = ''
            self.case_file = 'LF'
            self.data_path = 'AvaS_3000.npy'
    args = Parser()
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    seeds = list(map(int, args.seeds.strip('[]').split(',')))

    log_datetime = datetime.now()

    for i in range(len(seeds)):
        log_exp_name = 'debug'
        if args.exp == 'run':
            log_exp_name = args.env_id + '_' + args.mode + '_' + args.algo
            if args.mode == 'human':
                if args.use_baseline_ask != '':
                    log_exp_name = log_exp_name + '_' + args.use_baseline_ask
                if args.use_baseline_ask == 'diff' or args.use_baseline_ask == 'var':
                    log_exp_name = log_exp_name + '_th' + str(args.ask_threshold)
            if args.info != '':
                log_exp_name = log_exp_name + '_' + args.info
            log_exp_name = log_exp_name + '_' + str(seeds[i])
        log_date_dir = os.path.join('askrl', 'exp_v1', log_datetime.strftime('%Y-%m-%d_') + log_exp_name)
        args.log_dir = os.path.join(log_date_dir, log_datetime.strftime('%H-%M-%S'))
        args.seed = seeds[i]

        if(flag=='train'):  train(args, learner_id)
        if(flag=='test'):   test(args)

if __name__ == '__main__':
    main('train')