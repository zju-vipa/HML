import os
import sys
# sys.path.append("askrl")
ABSPATH = os.path.abspath(os.path.realpath(os.path.dirname(__file__)))
sys.path.append(ABSPATH)
from stable_baselines3.a2c import A2C
from stable_baselines3.ddpg import DDPG
from stable_baselines3.dqn import DQN
from stable_baselines3.her import HER
from stable_baselines3.ppo import PPO
from stable_baselines3.askppo import AskPPO
from stable_baselines3.aska2c import AskA2C
from stable_baselines3.sac import SAC
from stable_baselines3.td3 import TD3
from stable_baselines3.htac import HTAC

# Read version from file
version_file = os.path.join(os.path.dirname(__file__), "version.txt")
with open(version_file, "r") as file_handler:
    __version__ = file_handler.read().strip()
