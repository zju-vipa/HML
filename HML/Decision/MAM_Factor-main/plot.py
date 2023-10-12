import numpy as np
import matplotlib.pyplot as plt

def plot_q_table_heatmap(file_path):


    with open(file_path, "r") as file:
        lines = file.readlines()


    actions = []
    temp_actions = []


    for line in lines:
        if "State" in line:
            if temp_actions:
                actions.append(temp_actions)
                temp_actions = []
        elif "Action" in line:
            q_value = float(line.split('=')[-1].strip())
            temp_actions.append(q_value)


    if temp_actions:
        actions.append(temp_actions)


    q_table = np.array(actions)


    fig, ax = plt.subplots(figsize=(15, 15))
    cax = ax.matshow(q_table, cmap='viridis')


    fig.colorbar(cax)


    num_actions = q_table.shape[1]
    num_states = q_table.shape[0]

    ax.set_xticks(np.arange(0, num_actions, max(1, num_actions // 10)))
    ax.set_yticks(np.arange(0, num_states, max(1, num_states // 10)))
    ax.set_xticklabels(np.arange(0, num_actions, max(1, num_actions // 10)))
    ax.set_yticklabels(np.arange(0, num_states, max(1, num_states // 10)))
    ax.set_xlabel("Actions")
    ax.set_ylabel("States")
    ax.set_title("Q-Table Heatmap")

    plt.savefig("/root/HML/Decision/MAM_Factor-main/q_table/q_table.png")

    #plt.show()

