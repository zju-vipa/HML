import gym
import os
import sys
from service import LearnerService
from service import DatasetService
learnerService = LearnerService()
datasetService = DatasetService()
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
sys.path.append(ABSPATH)
# print(sys.path)
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from askrl.stable_baselines3 import PPO, AskPPO, DQN
from askrl.stable_baselines3.common.monitor import Monitor
from askrl.stable_baselines3.common.utils import linear_schedule
from askrl.stable_baselines3.common.callbacks import CheckpointCallback
from askrl.stable_baselines3.common.evaluation import evaluate_policy
from env.transmission_section import TransmissionSectionEnv


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


def get_human_policy():
    # model_path = "askrl/exp_v1/2021-11-12_PSASP300_vanilla_ppo_reward_gen_404/18-41-07/rl_model_final.zip"
    # model = PPO.load(model_path)

    def human_policy(state):
        # action, _ = model.predict(state.cpu(), deterministic=True)
        state = state.cpu().numpy()
        print("P:")
        print(state[0::4])
        print("Q:")
        print(state[1::4])
        print("V:")
        print(state[2::4])
        print("Theta:")
        print(state[3::4])
        #action = input("Human Action:")
        learner = learnerService.queryLearnerById(learner_id)
        # todo need change to a while lop waiting for the DB write the action
        # DB write  action = -1
        while (1==1):
            import  time
            time.sleep(10)
            action = #db query
            if(action!=-1): break
        return action

    return human_policy


def train(args):
    env = get_env(args)
    model = get_model(env, args)

    if args.use_baseline_ask != '':
        model.use_ask_loss = False

    if args.mode == 'human':
        model.human_policy = get_human_policy()   #不用就改成none

    checkpoint_callback = CheckpointCallback(save_freq=5000, save_path=args.log_dir, name_prefix='rl_model')
    model.learn(total_timesteps=args.total_timesteps, callback=checkpoint_callback, reset_num_timesteps=True)
    #model.learn(total_timesteps=args.total_timesteps, callback=checkpoint_callback, reset_num_timesteps=True)
   # print(args.log_dir)
   # model.save(os.path.join(args.log_dir, 'rl_model_final'))
    model.save(os.path.join('rl_model_final'))

def test(args):   # test时不会向人类提问
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
    return mean_reward   # todo
def main(flag = 'train'):
    class Parser():
        def __init__(self):
            self.env_id = 'case118'
            #self.mode = 'human'
            self.mode = 'vanilla'
            self.algo = 'ppo'
            #self.total_timesteps = int(5e4)
            self.total_timesteps = int(1e2)
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

        if(flag=='train'):  train(args)
        if(flag=='test'):   test(args)

if __name__ == '__main__':
    main('test')