from askrl.stable_baselines3.ppo.ppo import PPO
from askrl.stable_baselines3.common.env_util import make_vec_env
from askrl.stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from askrl.stable_baselines3.common.vec_env.subproc_vec_env import SubprocVecEnv
# import gym
import torch, numpy, gym

#from thermal_case import thermal_case
from PSASPEnv_v2 import PSASPEnv
import argparse
import os
import datetime
import time
import sys

from PSASPEnv_v2 import copy_dirs


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work_dir", default=r'/root/psasp/', type=str, help="file of work_dir")
    parser.add_argument("--source_dir", default=r"/root/psasp/", type=str, help="files of LF.*L")
    parser.add_argument("--case_file", default='LF', type=str, help="case_files_name")
    parser.add_argument("--data_path", default='NormalS_wj.npy', type=str, help="load_flu_dir")
    parser.add_argument("--is_training", type=bool, default=True, help="copy lf files, only training")
    args = parser.parse_args()
    return args


# 0.构建电网环境
save_dir = "./final_model/PPO"
args = get_args()
env_name = "PSASP3000-v0"


if __name__ == "__main__":
    wy_start_time = time.time()
    n_cpu = 6
    batch_size = 64
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    env = PSASPEnv(args)
    model = PPO("MlpPolicy",
                env,
                policy_kwargs=dict(net_arch=[dict(pi=[256, 256], vf=[256, 256])]),
                n_steps=batch_size * 12 // n_cpu,
                batch_size=batch_size,
                n_epochs=1,
                learning_rate=5e-4,
                gamma=0.8,
                verbose=2
                )
    model.learn(total_timesteps=int(5e4))
    cur_time=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model.save(f"Model_{cur_time}")
    model.load(f"Model_{cur_time}")
    # model.load(f"Model.zip")
    for _ in range(1):
        obs = env.reset(None, flag = True)
        done = False
        while not done:
            action, _ = model.predict(obs)  # print(action)
            obs, reward, done, info = env.step(action)  # env.render()
