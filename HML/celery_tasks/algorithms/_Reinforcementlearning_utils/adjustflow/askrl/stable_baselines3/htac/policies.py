from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import dgl
import gym
import numpy as np

import torch
import torch as th
from torch import nn

from stable_baselines3.common.policies import BasePolicy, register_policy
from stable_baselines3.common.distributions import Distribution, make_proba_distribution
from stable_baselines3.common.preprocessing import preprocess_obs

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor, GIN, GCN, MlpShareExtractor, NatureCNN
from stable_baselines3.common.type_aliases import Schedule
from stable_baselines3.common.utils import get_device


class MlpSingleExtractor(nn.Module):
    def __init__(
            self,
            feature_dim: int,
            net_arch: List[int],
            activation_fn: Type[nn.Module],
            device: Union[th.device, str] = "auto",
    ):
        super(MlpSingleExtractor, self).__init__()
        device = get_device(device)

        net = [nn.Linear(feature_dim, net_arch[0]), activation_fn()]

        for idx in range(len(net_arch) - 1):
            net.append(nn.Linear(net_arch[idx], net_arch[idx + 1]))
            net.append(activation_fn())

        # Save dim, used to create the distributions
        self.latent_dim = net_arch[-1]

        self.net = nn.Sequential(*net).to(device)

    def forward(self, features: th.Tensor) -> th.Tensor:
        return self.net(features)


class ActorCriticHierarchicalTreePolicy(BasePolicy):
    def __init__(
            self,
            observation_space: gym.spaces.Space,
            action_space: gym.spaces.Space,
            lr_schedule: Schedule,
            net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
            activation_fn: Type[nn.Module] = nn.Tanh,
            ortho_init: bool = True,
            use_sde: bool = False,
            features_extractor_class: Type[BaseFeaturesExtractor] = MlpShareExtractor,
            features_extractor_kwargs: Optional[Dict[str, Any]] = None,
            normalize_images: bool = True,
            optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
            optimizer_kwargs: Optional[Dict[str, Any]] = None,
            hiera_arch: List[int] = None,
            hiera_switch_action_top_down: bool = True,
            hiera_use_low_feature: bool = False,
    ):

        if optimizer_kwargs is None:
            optimizer_kwargs = {}

            if optimizer_class == th.optim.Adam:
                optimizer_kwargs["eps"] = 1e-5

        super(ActorCriticHierarchicalTreePolicy, self).__init__(
            observation_space,
            action_space,
            features_extractor_class,
            features_extractor_kwargs,
            optimizer_class=optimizer_class,
            optimizer_kwargs=optimizer_kwargs
        )

        self.hiera_arch = hiera_arch
        self.hiera_num = len(hiera_arch)
        assert self.hiera_num, "hiera_arch must be set"

        self.hiera_switch_action_top_down = hiera_switch_action_top_down
        self.hiera_use_low_feature = hiera_use_low_feature
        if features_extractor_class not in [GIN, GCN]:
            assert not self.hiera_use_low_feature, "No low features can be use"

        hiera_action_spaces = []
        for i in range(self.hiera_num):
            hiera_action_spaces.append(gym.spaces.Discrete(n=hiera_arch[i]))

        if net_arch is None:
            net_arch = [64, 64]

        self.net_arch = net_arch
        self.activation_fn = activation_fn
        self.ortho_init = ortho_init
        self.use_sde = use_sde
        self.normalize_images = normalize_images

        self.features_extractor = features_extractor_class(self.observation_space, **self.features_extractor_kwargs)

        self.pi_feature_dims = []
        self.pi_feature_dims.append(self.features_extractor.features_dim)
        self.pi_feature_dims.append(self.features_extractor.features_dim)

        if self.hiera_use_low_feature:
            self.pi_feature_dims.append(self.features_extractor.hidden_dim)
        else:
            self.pi_feature_dims.append(self.features_extractor.features_dim)

        self.vf_feature_dim = self.features_extractor.features_dim

        # Action distribution
        self.action_dists = [make_proba_distribution(hiera_action_spaces[i]) for i in range(self.hiera_num)]

        self._build(lr_schedule)

    def _get_constructor_parameters(self) -> Dict[str, Any]:
        data = super()._get_constructor_parameters()

        data.update(
            dict(
                net_arch=self.net_arch,
                activation_fn=self.activation_fn,
                lr_schedule=self._dummy_schedule,
                ortho_init=self.ortho_init,
                optimizer_class=self.optimizer_class,
                optimizer_kwargs=self.optimizer_kwargs,
                features_extractor_class=self.features_extractor_class,
                features_extractor_kwargs=self.features_extractor_kwargs,
            )
        )
        return data

    def _build_hiera_mlp_extractor(self) -> None:
        self.pi_mlp_extractor_hazard = MlpSingleExtractor(
            self.pi_feature_dims[0], net_arch=self.net_arch, activation_fn=self.activation_fn, device=self.device
        )
        self.pi_mlp_extractor_node = MlpSingleExtractor(
            self.pi_feature_dims[1], net_arch=self.net_arch, activation_fn=self.activation_fn, device=self.device
        )
        self.pi_mlp_extractor_set = MlpSingleExtractor(
            self.pi_feature_dims[2], net_arch=self.net_arch, activation_fn=self.activation_fn, device=self.device
        )
        self.vf_mlp_extractor = MlpSingleExtractor(
            self.vf_feature_dim, net_arch=self.net_arch, activation_fn=self.activation_fn, device=self.device
        )

    def _build(self, lr_schedule: Schedule) -> None:
        self._build_hiera_mlp_extractor()

        self.action_net_hazard = self.action_dists[0].proba_distribution_net(self.pi_mlp_extractor_hazard.latent_dim)
        self.action_net_node = self.action_dists[1].proba_distribution_net(self.pi_mlp_extractor_node.latent_dim)
        self.action_net_set = self.action_dists[2].proba_distribution_net(self.pi_mlp_extractor_set.latent_dim)

        self.value_net = nn.Linear(self.vf_mlp_extractor.latent_dim, 1)

        if self.ortho_init:
            module_gains = {
                self.features_extractor: np.sqrt(2),
                self.vf_mlp_extractor: np.sqrt(2),
                self.pi_mlp_extractor_hazard: np.sqrt(2),
                self.pi_mlp_extractor_node: np.sqrt(2),
                self.pi_mlp_extractor_set: np.sqrt(2),
                self.value_net: 1,
                self.action_net_hazard: 0.01,
                self.action_net_node: 0.01,
                self.action_net_set: 0.01,
            }

            for module, gain in module_gains.items():
                module.apply(partial(self.init_weights, gain=gain))

        # Setup optimizer with initial learning rate
        self.optimizer = self.optimizer_class(self.parameters(), lr=lr_schedule(1), **self.optimizer_kwargs)

    def forward(self, obs: th.Tensor, deterministic: bool = False) -> Tuple[th.Tensor, th.Tensor, th.Tensor]:
        top_features, low_features = self.extract_features(obs)

        actions, log_prob = self._get_actions(top_features, low_features)
        latent_vf = self.vf_mlp_extractor(top_features)
        values = self.value_net(latent_vf)

        return actions, values, log_prob

    def extract_features(self, obs: th.Tensor):
        assert self.features_extractor is not None, "No features extractor was set"
        preprocessed_obs = preprocess_obs(obs, self.observation_space, normalize_images=self.normalize_images)

        if self.hiera_use_low_feature:
            top_features, low_features = self.features_extractor(preprocessed_obs, use_low_feature=True)
        else:
            features = self.features_extractor(preprocessed_obs)
            top_features = features
            low_features = features

        return top_features, low_features

    def _get_actions(self, top_features: th.Tensor, low_features: th.Tensor):
        actions_hazard, log_prob_hazard, distribution_hazard = self._one_policy_forward(0, top_features)
        actions_node, log_prob_node, distribution_node = self._one_policy_forward(1, top_features)

        batch_size = top_features.shape[0]
        if self.hiera_use_low_feature:
            low_features = low_features[list(range(batch_size)), actions_node.long(), :]

        actions_set, log_prob_set, distribution_set = self._one_policy_forward(2, low_features)

        if self.hiera_switch_action_top_down:
            # ==================== actions = [node 0 set all, ..., node N set all] start ====================
            actions = actions_hazard * (1 + actions_node * self.hiera_arch[2] + actions_set)
            # ==================== actions = [node 0 set all, ..., node N set all] end ====================
        else:
            # ==================== actions = [all node set 0, ..., all node set N] start ====================
            actions = actions_hazard * (1 + actions_node + actions_set * self.hiera_arch[1])
            # ==================== actions = [all node set 0, ..., all node set N] end ====================

        log_prob = log_prob_hazard + actions_hazard * (log_prob_node + log_prob_set)

        return actions, log_prob

    def _one_policy_forward(self, policy_index: int, features: th.Tensor, deterministic: bool = False):
        if policy_index == 0:
            latent_pi = self.pi_mlp_extractor_hazard(features)
        elif policy_index == 1:
            latent_pi = self.pi_mlp_extractor_node(features)
        elif policy_index == 2:
            latent_pi = self.pi_mlp_extractor_set(features)
        else:
            assert False, "Policy index not exist"

        distribution = self._get_action_dist_from_latent(policy_index, latent_pi)
        actions = distribution.get_actions(deterministic=deterministic)
        log_prob = distribution.log_prob(actions)

        return actions, log_prob, distribution

    def _one_policy_evaluate_actions(self, policy_index: int, features: th.Tensor, actions: th.Tensor):
        if policy_index == 0:
            latent_pi = self.pi_mlp_extractor_hazard(features)
        elif policy_index == 1:
            latent_pi = self.pi_mlp_extractor_node(features)
        elif policy_index == 2:
            latent_pi = self.pi_mlp_extractor_set(features)
        else:
            assert False, "Policy index not exist"

        distribution = self._get_action_dist_from_latent(policy_index, latent_pi)
        log_prob = distribution.log_prob(actions)

        return log_prob, distribution.distribution

    def _get_action_dist_from_latent(self, policy_index: int, latent_pi: th.Tensor) -> Distribution:
        if policy_index == 0:
            mean_actions = self.action_net_hazard(latent_pi)
        elif policy_index == 1:
            mean_actions = self.action_net_node(latent_pi)
        elif policy_index == 2:
            mean_actions = self.action_net_set(latent_pi)
        else:
            assert False, "Policy index not exist"

        return self.action_dists[policy_index].proba_distribution(action_logits=mean_actions)

    def _predict(self, obs: th.Tensor, deterministic: bool = False) -> th.Tensor:
        top_features, low_features = self.extract_features(obs)

        actions, _ = self._get_actions(top_features, low_features)

        return actions

    def _get_entropy(self, top_features: th.Tensor, low_features: th.Tensor, actions: th.Tensor):
        if self.hiera_switch_action_top_down:
            # ==================== actions = [node 0 set all, ..., node N set all] start ====================
            actions_hazard = torch.tensor(actions != 0, dtype=th.int64)
            actions_node = torch.abs(torch.floor((actions - 1) / self.hiera_arch[2]))
            actions_set = (actions - 1) % self.hiera_arch[2]
            # ==================== actions = [node 0 set all, ..., node N set all] end ====================
        else:
            # ==================== actions = [all node set 0, ..., all node set N] start ====================
            actions_hazard = torch.tensor(actions != 0, dtype=th.int64)
            actions_node = (actions - 1) % self.hiera_arch[1]
            actions_set = torch.abs(torch.floor((actions - 1) / self.hiera_arch[1]))
            # ==================== actions = [all node set 0, ..., all node set N] end ====================

        log_prob_hazard, distribution_hazard = self._one_policy_evaluate_actions(0, top_features, actions_hazard)
        log_prob_node, distribution_node = self._one_policy_evaluate_actions(1, top_features, actions_node)

        batch_size = top_features.shape[0]
        if self.hiera_use_low_feature:
            low_features = low_features[list(range(batch_size)), actions_node.long(), :]

        log_prob_set, distribution_set = self._one_policy_evaluate_actions(2, low_features, actions_set)

        log_prob = log_prob_hazard + actions_hazard * (log_prob_node + log_prob_set)

        probs = torch.zeros((batch_size, 1 + self.hiera_arch[1] * self.hiera_arch[2]), dtype=torch.float32).to(self.device)
        logits = torch.zeros((batch_size, 1 + self.hiera_arch[1] * self.hiera_arch[2]), dtype=torch.float32).to(self.device)

        probs[:, 0] = distribution_hazard.probs[:, 0]
        logits[:, 0] = distribution_hazard.logits[:, 0]

        if self.hiera_switch_action_top_down:
            # ==================== actions = [node 0 set all, ..., node N set all] start ====================
            for i in range(self.hiera_arch[2]):
                probs[:, i + 1::self.hiera_arch[2]] = distribution_hazard.probs[:, 1].unsqueeze(1) * distribution_node.probs * distribution_set.probs[:, i].unsqueeze(1)
                logits[:, i + 1::self.hiera_arch[2]] = distribution_hazard.probs[:, 1].unsqueeze(1) + distribution_node.probs + distribution_set.probs[:, i].unsqueeze(1)
            # ==================== actions = [node 0 set all, ..., node N set all] end ====================
        else:
            # ==================== actions = [all node set 0, ..., all node set N] start ====================
            for i in range(self.hiera_arch[2]):
                probs[:, i * self.hiera_arch[1] + 1:(i + 1) * self.hiera_arch[1] + 1] = distribution_hazard.probs[:, 1].unsqueeze(1) * distribution_node.probs * distribution_set.probs[:, i].unsqueeze(1)
                logits[:, i * self.hiera_arch[1] + 1:(i + 1) * self.hiera_arch[1] + 1] = distribution_hazard.probs[:, 1].unsqueeze(1) + distribution_node.probs + distribution_set.probs[:, i].unsqueeze(1)
            # ==================== actions = [all node set 0, ..., all node set N] end ====================

        min_real = torch.finfo(logits.dtype).min
        logits = torch.clamp(logits, min=min_real)
        p_log_p = logits * probs
        entropy = -p_log_p.sum(-1)

        return log_prob, entropy

    def evaluate_actions(self, obs: th.Tensor, actions: th.Tensor):
        top_features, low_features = self.extract_features(obs)

        latent_vf = self.vf_mlp_extractor(top_features)
        values = self.value_net(latent_vf)

        log_prob, entropy = self._get_entropy(top_features, low_features, actions)

        return values, log_prob, entropy


class ActorCriticHierarchicalTreeCnnPolicy(ActorCriticHierarchicalTreePolicy):
    def __init__(
            self,
            observation_space: gym.spaces.Space,
            action_space: gym.spaces.Space,
            lr_schedule: Schedule,
            net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
            activation_fn: Type[nn.Module] = nn.Tanh,
            ortho_init: bool = True,
            use_sde: bool = False,
            features_extractor_class: Type[BaseFeaturesExtractor] = NatureCNN,
            features_extractor_kwargs: Optional[Dict[str, Any]] = None,
            normalize_images: bool = True,
            optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
            optimizer_kwargs: Optional[Dict[str, Any]] = None,
            hiera_arch: List[int] = None,
            hiera_switch_action_top_down: bool = True,
            hiera_use_low_feature: bool = False,
    ):
        super(ActorCriticHierarchicalTreeCnnPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            ortho_init,
            use_sde,
            features_extractor_class,
            features_extractor_kwargs,
            normalize_images,
            optimizer_class,
            optimizer_kwargs,
            hiera_arch,
            hiera_switch_action_top_down,
            hiera_use_low_feature
        )


class ActorCriticHierarchicalTreeGnnPolicy(ActorCriticHierarchicalTreePolicy):
    def __init__(
            self,
            observation_space: gym.spaces.Space,
            action_space: gym.spaces.Space,
            lr_schedule: Schedule,
            net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
            activation_fn: Type[nn.Module] = nn.Tanh,
            ortho_init: bool = True,
            use_sde: bool = False,
            features_extractor_class: Type[BaseFeaturesExtractor] = GCN,
            features_extractor_kwargs: Optional[Dict[str, Any]] = None,
            normalize_images: bool = True,
            optimizer_class: Type[th.optim.Optimizer] = th.optim.Adam,
            optimizer_kwargs: Optional[Dict[str, Any]] = None,
            hiera_arch: List[int] = None,
            hiera_switch_action_top_down: bool = True,
            hiera_use_low_feature: bool = False,
    ):
        super(ActorCriticHierarchicalTreeGnnPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            ortho_init,
            use_sde,
            features_extractor_class,
            features_extractor_kwargs,
            normalize_images,
            optimizer_class,
            optimizer_kwargs,
            hiera_arch,
            hiera_switch_action_top_down,
            hiera_use_low_feature
        )


register_policy("MlpPolicy", ActorCriticHierarchicalTreePolicy)
register_policy("CnnPolicy", ActorCriticHierarchicalTreeCnnPolicy)
register_policy("GnnPolicy", ActorCriticHierarchicalTreeGnnPolicy)
