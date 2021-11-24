import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import gym
import numpy as np
import torch as th

from stable_baselines3.common import logger
from stable_baselines3.common.base_class import BaseAlgorithm
from stable_baselines3.common.buffers import RolloutAskBuffer
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.policies import ActorCriticPolicy
from stable_baselines3.common.type_aliases import GymEnv, MaybeCallback, Schedule
from stable_baselines3.common.utils import safe_mean
from stable_baselines3.common.vec_env import VecEnv


class OnAskPolicyAlgorithm(BaseAlgorithm):
    """
    The base for On-Ask-Policy algorithms (ex: Ask PPO).

    :param policy: The policy model to use (MlpPolicy, CnnPolicy, ...)
    :param env: The environment to learn from (if registered in Gym, can be str)
    :param learning_rate: The learning rate, it can be a function
        of the current progress remaining (from 1 to 0)
    :param n_steps: The number of steps to run for each environment per update
        (i.e. batch size is n_steps * n_env where n_env is number of environment copies running in parallel)
    :param gamma: Discount factor
    :param gae_lambda: Factor for trade-off of bias vs variance for Generalized Advantage Estimator.
        Equivalent to classic advantage when set to 1.
    :param ent_coef: Entropy coefficient for the loss calculation
    :param vf_coef: Value function coefficient for the loss calculation
    :param max_grad_norm: The maximum value for the gradient clipping
    :param use_sde: Whether to use generalized State Dependent Exploration (gSDE)
        instead of action noise exploration (default: False)
    :param sde_sample_freq: Sample a new noise matrix every n steps when using gSDE
        Default: -1 (only sample at the beginning of the rollout)
    :param tensorboard_log: the log location for tensorboard (if None, no logging)
    :param create_eval_env: Whether to create a second environment that will be
        used for evaluating the agent periodically. (Only available when passing string for the environment)
    :param monitor_wrapper: When creating an environment, whether to wrap it
        or not in a Monitor wrapper.
    :param policy_kwargs: additional arguments to be passed to the policy on creation
    :param verbose: the verbosity level: 0 no output, 1 info, 2 debug
    :param seed: Seed for the pseudo random generators
    :param device: Device (cpu, cuda, ...) on which the code should be run.
        Setting it to auto, the code will be run on the GPU if possible.
    :param _init_setup_model: Whether or not to build the network at the creation of the instance
    :param human_model: Whether or not to build the network at the creation of the instance
    """

    def __init__(
        self,
        policy: Union[str, Type[ActorCriticPolicy]],
        env: Union[GymEnv, str],
        learning_rate: Union[float, Schedule],
        n_steps: int,
        gamma: float,
        gae_lambda: float,
        ent_coef: float,
        vf_coef: float,
        max_grad_norm: float,
        use_sde: bool,
        sde_sample_freq: int,
        tensorboard_log: Optional[str] = None,
        create_eval_env: bool = False,
        monitor_wrapper: bool = True,
        policy_kwargs: Optional[Dict[str, Any]] = None,
        verbose: int = 0,
        seed: Optional[int] = None,
        device: Union[th.device, str] = "auto",
        human_policy: Callable = None,
        use_ask_loss: bool = True,
        use_baseline_ask: str = '',
        ask_threshold:  float = 0.2,
        _init_setup_model: bool = True,
    ):

        super(OnAskPolicyAlgorithm, self).__init__(
            policy=policy,
            env=env,
            policy_base=ActorCriticPolicy,
            learning_rate=learning_rate,
            policy_kwargs=policy_kwargs,
            verbose=verbose,
            device=device,
            use_sde=use_sde,
            sde_sample_freq=sde_sample_freq,
            create_eval_env=create_eval_env,
            support_multi_env=True,
            seed=seed,
            tensorboard_log=tensorboard_log,
        )

        self.n_steps = n_steps
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.ent_coef = ent_coef
        self.vf_coef = vf_coef
        self.max_grad_norm = max_grad_norm
        self.rollout_buffer = None
        self.human_policy = human_policy
        self.use_ask_loss = use_ask_loss
        self.use_baseline_ask = use_baseline_ask
        self.ask_threshold = ask_threshold

        # # =================== identification mechanism for human mistakes start ===================
        # self.cnt_random_human_action = 0
        # self.cnt_find_random_human_action = 0
        # self.ratio_find_random_human_action = 0.0
        # # =================== identification mechanism for human mistakes end ===================

        if _init_setup_model:
            self._setup_model()

    def _setup_model(self) -> None:
        self._setup_lr_schedule()
        self.set_random_seed(self.seed)

        self.rollout_buffer = RolloutAskBuffer(
            self.n_steps,
            self.observation_space,
            self.action_space,
            self.device,
            gamma=self.gamma,
            gae_lambda=self.gae_lambda,
            n_envs=self.n_envs,
        )
        self.policy = self.policy_class(
            self.observation_space,
            self.action_space,
            self.lr_schedule,
            use_sde=self.use_sde,
            **self.policy_kwargs  # pytype:disable=not-instantiable
        )
        self.policy = self.policy.to(self.device)

    def collect_rollouts(
        self, env: VecEnv, callback: BaseCallback, rollout_buffer: RolloutAskBuffer, n_rollout_steps: int
    ) -> bool:
        """
        Collect experiences using the current policy and fill a ``RolloutAskBuffer``.
        The term rollout here refers to the model-free notion and should not
        be used with the concept of rollout used in model-based RL or planning.

        :param env: The training environment
        :param callback: Callback that will be called at each step
            (and at the beginning and end of the rollout)
        :param rollout_buffer: Buffer to fill with rollouts
        :param n_steps: Number of experiences to collect per environment
        :return: True if function returned with at least `n_rollout_steps`
            collected, False if callback terminated rollout prematurely.
        """
        assert self._last_obs is not None, "No previous observation was provided"
        n_steps = 0
        rollout_buffer.reset()
        # Sample new weights for the state dependent exploration
        if self.use_sde:
            self.policy.reset_noise(env.num_envs)

        callback.on_rollout_start()

        while n_steps < n_rollout_steps:
            if self.use_sde and self.sde_sample_freq > 0 and n_steps % self.sde_sample_freq == 0:
                # Sample a new noise matrix
                self.policy.reset_noise(env.num_envs)

            with th.no_grad():
                # Convert to pytorch tensor
                obs_tensor = th.as_tensor(self._last_obs).to(self.device)
                actions, values, log_probs = self.policy.forward(obs_tensor)

                # =================== ask human start ===================

                human_actions = np.array([-1] * env.num_envs, dtype=np.int64)

                if self.use_baseline_ask == 'diff' or self.use_baseline_ask == 'var':
                    latent_pi, _, latent_sde = self.policy._get_latent(obs_tensor)
                    distribution = self.policy._get_action_dist_from_latent(latent_pi, latent_sde)
                    prob = distribution.distribution.probs

                for i in range(env.num_envs):
                    if self.use_baseline_ask == 'cm':
                        human_actions[i] = self.human_policy(obs_tensor[i])
                    elif self.use_baseline_ask == 'diff':
                        if prob[i].max() - prob[i].min() < self.ask_threshold:
                            human_actions[i] = self.human_policy(obs_tensor[i])
                    elif self.use_baseline_ask == 'var':
                        if prob[i].var() < self.ask_threshold:
                            human_actions[i] = self.human_policy(obs_tensor[i])
                    elif actions[i] == env.action_space.n - 1:
                        human_actions[i] = self.human_policy(obs_tensor[i])

                # =================== ask human end ===================

                # # =================== identification mechanism for human mistakes start ===================
                #
                # human_actions = np.array([-1] * env.num_envs, dtype=np.int64)
                # is_randoms = np.array([False] * env.num_envs, dtype=np.bool)
                # for i in range(env.num_envs):
                #     if self.use_baseline_ask == 'cm':
                #         human_actions[i] = self.human_policy(obs_tensor[i])
                #     elif actions[i] == env.action_space.n - 1:
                #         human_actions[i], is_randoms[i] = self.human_policy(obs_tensor[i], return_is_random=True)
                #         if is_randoms[i]:
                #             self.cnt_random_human_action += 1
                #
                # # identify human mistakes
                # latent_pi, _, latent_sde = self.policy._get_latent(obs_tensor)
                # distribution = self.policy._get_action_dist_from_latent(latent_pi, latent_sde)
                # probs = distribution.distribution.probs
                #
                # ask_logits = distribution.distribution.logits
                # ask_p_log_p = ask_logits * probs
                # ask_entropy = -ask_p_log_p.sum(-1)
                # ask_normalized_entropy = ask_entropy / np.log(env.action_space.n)
                #
                # probs = th.nn.functional.softmax(probs[:, :env.action_space.n - 1], dim=1)
                # logits = th.log(probs)
                # p_log_p = logits * probs
                # entropy = -p_log_p.sum(-1)
                # min_action = th.argmin(probs, dim=1)
                # max_action = th.argmax(probs, dim=1)
                #
                # normalized_entropy = entropy / np.log(env.action_space.n - 1)
                #
                # for i in range(env.num_envs):
                #     if actions[i] == env.action_space.n - 1:
                #         if human_actions[i] == min_action[i] and normalized_entropy[i] < ask_normalized_entropy[i]:
                #             human_actions[i] = max_action[i]
                #             if is_randoms[i]:
                #                 self.cnt_find_random_human_action += 1
                #
                # # =================== identification mechanism for human mistakes end ===================

            actions = actions.cpu().numpy()

            # Rescale and perform action
            clipped_actions = actions
            # Clip the actions to avoid out of bound error
            if isinstance(self.action_space, gym.spaces.Box):
                clipped_actions = np.clip(actions, self.action_space.low, self.action_space.high)

            final_actions = clipped_actions

            if self.use_baseline_ask == '':
                for i in range(env.num_envs):
                    if human_actions[i] != -1:
                        final_actions[i] = human_actions[i]

            new_obs, rewards, dones, infos = env.step(final_actions)

            self.num_timesteps += env.num_envs

            # Give access to local variables
            callback.update_locals(locals())
            if callback.on_step() is False:
                return False

            self._update_info_buffer(infos)
            n_steps += 1

            if isinstance(self.action_space, gym.spaces.Discrete):
                # Reshape in case of discrete action
                actions = actions.reshape(-1, 1)
                human_actions = human_actions.reshape(-1, 1)

            rollout_buffer.add(self._last_obs, actions, human_actions, rewards, self._last_dones, values, log_probs)
            self._last_obs = new_obs
            self._last_dones = dones

        with th.no_grad():
            # Compute value for the last timestep
            obs_tensor = th.as_tensor(new_obs).to(self.device)
            _, values, _ = self.policy.forward(obs_tensor)

        rollout_buffer.compute_returns_and_advantage(last_values=values, dones=dones)

        callback.on_rollout_end()

        return True

    def train(self) -> None:
        """
        Consume current rollout data and update policy parameters.
        Implemented by individual algorithms.
        """
        raise NotImplementedError

    def learn(
        self,
        total_timesteps: int,
        callback: MaybeCallback = None,
        log_interval: int = 1,
        eval_env: Optional[GymEnv] = None,
        eval_freq: int = -1,
        n_eval_episodes: int = 5,
        tb_log_name: str = "OnAskPolicyAlgorithm",
        eval_log_path: Optional[str] = None,
        reset_num_timesteps: bool = True,
    ) -> "OnAskPolicyAlgorithm":
        iteration = 0

        total_timesteps, callback = self._setup_learn(
            total_timesteps, eval_env, callback, eval_freq, n_eval_episodes, eval_log_path, reset_num_timesteps, tb_log_name
        )

        callback.on_training_start(locals(), globals())

        while self.num_timesteps < total_timesteps:

            continue_training = self.collect_rollouts(self.env, callback, self.rollout_buffer, n_rollout_steps=self.n_steps)

            if continue_training is False:
                break

            iteration += 1
            self._update_current_progress_remaining(self.num_timesteps, total_timesteps)

            # Display training infos
            if log_interval is not None and iteration % log_interval == 0:
                fps = int(self.num_timesteps / (time.time() - self.start_time))
                logger.record("time/iterations", iteration, exclude="tensorboard")
                if len(self.ep_info_buffer) > 0 and len(self.ep_info_buffer[0]) > 0:
                    logger.record("rollout/ep_rew_mean", safe_mean([ep_info["r"] for ep_info in self.ep_info_buffer]))
                    logger.record("rollout/ep_len_mean", safe_mean([ep_info["l"] for ep_info in self.ep_info_buffer]))
                logger.record("time/fps", fps)
                logger.record("time/time_elapsed", int(time.time() - self.start_time), exclude="tensorboard")
                logger.record("time/total_timesteps", self.num_timesteps, exclude="tensorboard")

                # # =================== identification mechanism for human mistakes log start ===================
                # logger.record("random_human/cnt_random_human_action", self.cnt_random_human_action)
                # logger.record("random_human/cnt_find_random_human_action", self.cnt_find_random_human_action)
                #
                # if self.cnt_random_human_action != 0:
                #     self.ratio_find_random_human_action = self.cnt_find_random_human_action / self.cnt_random_human_action
                # logger.record("random_human/ratio_find_random_human_action", self.ratio_find_random_human_action)
                # # =================== identification mechanism for human mistakes log end ===================

                logger.dump(step=self.num_timesteps)

            self.train()

        callback.on_training_end()

        return self

    def _get_torch_save_params(self) -> Tuple[List[str], List[str]]:
        state_dicts = ["policy", "policy.optimizer"]

        return state_dicts, []
