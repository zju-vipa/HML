import torch
import numpy as np
from plot import plot_q_table_heatmap


class SoftNet(torch.nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SoftNet, self).__init__()
        self.base = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, output_dim)
        )

    def forward(self, x):
        return self.base(x)


# model_path = "log/M5case118/MAMAttention/policy.pth"
model_path = "/root/HML/Decision/MAM_Factor-main/log/M5case118/MAMAttention/policy.pth"
policy_data = torch.load(model_path, map_location=torch.device('cpu'))
soft_net = SoftNet(645, 106)
soft_net.load_state_dict(policy_data, strict=False)

class Box:
    def __init__(self, low, high, shape, dtype):
        self.low = np.array(low)
        self.high = np.array(high)
        self.shape = shape
        self.dtype = dtype


observation_space = Box(low=-1.0, high=1.0, shape=(645,), dtype=np.float32)


def generate_evenly_spaced_states(observation_space, num_samples=100):
    values = np.linspace(np.min(observation_space.low), np.max(observation_space.high), num_samples)
    states = np.array([np.full(observation_space.shape, value) for value in values])
    return states

sampled_states = generate_evenly_spaced_states(observation_space, num_samples=100)


q_values = []
for state in sampled_states:
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    q_value = soft_net.base(state_tensor).detach().numpy()
    q_values.append(q_value)


file_path = "/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt"
with open(file_path, 'w') as file:
    for state_idx, state in enumerate(sampled_states):
        file.write(f"State {state_idx}:\n")
        for action_idx, q_value in enumerate(q_values[state_idx][0]):
            file.write(f"Action {action_idx}: Q-value = {q_value}\n")
        file.write("\n")

plot_q_table_heatmap("/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt")

def run_q_table():
    import torch
    import numpy as np
    from plot import plot_q_table_heatmap


    class SoftNet(torch.nn.Module):
        def __init__(self, input_dim, output_dim):
            super(SoftNet, self).__init__()
            self.base = torch.nn.Sequential(
                torch.nn.Linear(input_dim, 256),
                torch.nn.ReLU(),
                torch.nn.Linear(256, 256),
                torch.nn.ReLU(),
                torch.nn.Linear(256, output_dim)
            )

        def forward(self, x):
            return self.base(x)


    model_path = "/root/HML/Decision/MAM_Factor-main/log/M5case118/MAMAttention/policy.pth"
    policy_data = torch.load(model_path, map_location=torch.device('cpu'))
    soft_net = SoftNet(645, 106)
    soft_net.load_state_dict(policy_data, strict=False)


    class Box:
        def __init__(self, low, high, shape, dtype):
            self.low = np.array(low)
            self.high = np.array(high)
            self.shape = shape
            self.dtype = dtype


    observation_space = Box(low=-1.0, high=1.0, shape=(645,), dtype=np.float32)


    def generate_evenly_spaced_states(observation_space, num_samples=100):
        values = np.linspace(np.min(observation_space.low), np.max(observation_space.high), num_samples)
        states = np.array([np.full(observation_space.shape, value) for value in values])
        return states

    sampled_states = generate_evenly_spaced_states(observation_space, num_samples=100)


    q_values = []
    for state in sampled_states:
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_value = soft_net.base(state_tensor).detach().numpy()
        q_values.append(q_value)


    file_path = "/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt"
    with open(file_path, 'w') as file:
        for state_idx, state in enumerate(sampled_states):
            file.write(f"State {state_idx}:\n")
            for action_idx, q_value in enumerate(q_values[state_idx][0]):
                file.write(f"Action {action_idx}: Q-value = {q_value}\n")
            file.write("\n")

    plot_q_table_heatmap("/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt")



# import torch
# import numpy as np
# from plot import plot_q_table_heatmap
# import os

# class SoftNet(torch.nn.Module):
#     def __init__(self, input_dim, output_dim):
#         super(SoftNet, self).__init__()
#         self.base = torch.nn.Sequential(
#             torch.nn.Linear(input_dim, 256),
#             torch.nn.ReLU(),
#             torch.nn.Linear(256, 256),
#             torch.nn.ReLU(),
#             torch.nn.Linear(256, output_dim)
#         )

#     def forward(self, x):
#         return self.base(x)


# log_dir = "/root/HML/Decision/MAM_Factor-main/log/"
# sub_dirs = [d for d in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, d))]
# if sub_dirs:
#     model_path = os.path.join(log_dir, sub_dirs[0], "MAMAttention/policy.pth")
# else:
#     raise FileNotFoundError("No subdirectory found in log directory")

# policy_data = torch.load(model_path, map_location=torch.device('cpu'))
# soft_net = SoftNet(645, 106)
# soft_net.load_state_dict(policy_data, strict=False)

# class Box:
#     def __init__(self, low, high, shape, dtype):
#         self.low = np.array(low)
#         self.high = np.array(high)
#         self.shape = shape
#         self.dtype = dtype


# observation_space = Box(low=-1.0, high=1.0, shape=(645,), dtype=np.float32)


# def generate_evenly_spaced_states(observation_space, num_samples=100):
#     values = np.linspace(np.min(observation_space.low), np.max(observation_space.high), num_samples)
#     states = np.array([np.full(observation_space.shape, value) for value in values])
#     return states

# sampled_states = generate_evenly_spaced_states(observation_space, num_samples=100)


# q_values = []
# for state in sampled_states:
#     state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
#     q_value = soft_net.base(state_tensor).detach().numpy()
#     q_values.append(q_value)


# file_path = "/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt"
# with open(file_path, 'w') as file:
#     for state_idx, state in enumerate(sampled_states):
#         file.write(f"State {state_idx}:\n")
#         for action_idx, q_value in enumerate(q_values[state_idx][0]):
#             file.write(f"Action {action_idx}: Q-value = {q_value}\n")
#         file.write("\n")

# plot_q_table_heatmap("/root/HML/Decision/MAM_Factor-main/q_table/q_table_evenly_spaced_states.txt")
