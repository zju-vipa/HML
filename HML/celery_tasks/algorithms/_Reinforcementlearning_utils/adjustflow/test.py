import argparse
import os
import time
import sys
import torch
import numpy as np
import gym
from datetime import datetime

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


def set(args, learner_id):
    env = get_env(args)
    model = get_model(env, args)

    if args.mode == 'human':
        model.human_policy = None
    model.load(args.model_name, env=env)
    return env, model


def main(flag = 'test', learner_id=None, mode='vanilla'):
    class Parser():
        def __init__(self):
            self.env_id = 'case300'
            self.mode = mode
            self.algo = 'ppo'
            self.total_timesteps = int(5e4)
            self.seeds = '[404]'
            self.info = 'reward_gen'
            self.gpu = '0'
            self.case_file = 'LF'
            self.data_dir = 'data'
            self.scence_file = 'scence.npy'
            self.model_name = 'final_ppo_model_1'
            self.test_epoch = 1
            self.is_training = True

    args = Parser()
    os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    seeds = list(map(int, args.seeds.strip('[]').split(',')))

    log_datetime = datetime.now()
    all_reward = 0

    for i in range(len(seeds)):
        log_exp_name = args.env_id + '_' + args.mode + '_' + args.algo + '_' + args.info
        log_exp_name = log_exp_name + '_' + str(seeds[i])
        args.work_dir = os.path.join('askrl', 'exp_v1', log_datetime.strftime('%Y-%m-%d-%H-%M-%S-') + log_exp_name)
        args.seed = seeds[i]

        if flag == 'test':
            copy_dirs(args.data_dir, args.work_dir)
            env, model = set(args, learner_id)
            for i in range(args.test_epoch):
                obs = env.reset()
                done = False
                sum_reward=0
                while not done:
                    action, _ = model.predict(obs, deterministic=False)  # print(action)
                    if model.__class__.__name__[:3] == 'Ask':
                        if action == env.action_space.n - 1:
                            human_action = np.random.randint(low=0, high=env.action_space.n - 1)
                            if isinstance(action, np.ndarray):
                                human_action = np.array([human_action])
                            action = human_action
                    obs, reward, done, info = env.step(action)  # env.render()
                    sum_reward+=reward
                all_reward+=sum_reward
                print(f"The {i}/{args.test_epoch} final reward: {sum_reward}")
                
    allinfo = all_reward/(args.test_epoch*len(seeds))
    file_directory = os.path.join(current_app.config["SAVE_L_MODEL_PATH"], learner_id)
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)
    file_name = 'test_info'
    file_path = os.path.join(file_directory, file_name)          
          
    np.save(file_path, allinfo)
                
    return all_reward/(args.test_epoch*len(seeds))

# if __name__ == '__main__':
#     main('test')