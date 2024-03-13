
import numpy as np
import torch
import networkx as nx
import pandas as pd
from tqdm import tqdm
from scipy.io import loadmat
import progressbar
class S2VGraph(object):
    def __init__(self, g, label, node_tags=None, node_features=None):
        '''
            g: a networkx graph
            label: an integer graph label
            node_tags: a list of integer node tags
            node_features: a torch float tensor, one-hot representation of the tag that is used as input to neural nets
            edge_mat: a torch long tensor, contain edge list, will be used to create torch sparse tensor
            neighbors: list of neighbors (without self-loop)
        '''
        self.label = label
        self.g = g
        self.node_tags = node_tags
        self.neighbors = []
        self.node_features = torch.tensor(node_features, dtype=torch.float32)
        self.edge_mat = 0

        self.max_neighbor = 0

def separate_data(g_list, num_sample, train_ratio):

    pos_num = len(g_list)//2
    pos_id = list(range(pos_num))
    neg_id = list(range(pos_num, len(g_list)))
    # np.random.shuffle(pos_id)F
    # np.random.shuffle(neg_id)
    train_num = int(num_sample * train_ratio)

    pos_trid = pos_id[0:train_num]
    pos_ttid = pos_id[train_num:num_sample]
    neg_trid = neg_id[0:train_num]
    neg_ttid = neg_id[train_num:num_sample]

    tr_id = []
    tr_id.extend(pos_trid)
    tr_id.extend(neg_trid)

    tt_id = []
    tt_id.extend(pos_ttid)
    tt_id.extend(neg_ttid)

    train_graphs = [g_list[i] for i in tr_id]
    test_graphs = [g_list[i] for i in tt_id]

    return train_graphs, test_graphs



def add_labels_edge(g_list):
    ii = 0
    for g in g_list:
        g.neighbors = [[] for i in range(len(g.g))]
        for i, j in g.g.edges():
            g.neighbors[i].append(j)
            g.neighbors[j].append(i)
        degree_list = []
        for i in range(len(g.g)):
            g.neighbors[i] = g.neighbors[i]
            degree_list.append(len(g.neighbors[i]))
        g.max_neighbor = max(degree_list)

        edges = [list(pair) for pair in g.g.edges()]
        edges.extend([[i, j] for j, i in edges])
        deg_list = list(dict(g.g.degree(range(len(g.g)))).values())
        g.edge_mat = torch.LongTensor(edges).transpose(0, 1)
        ii += 1
        #print(ii)
    return g_list



def loda_matdata_case39(dataset, fold_idx):
    print('开始导入电力系统数据...')

    data = loadmat('data/case39/case39.mat')
    bus_matrix = data['data']['bus_matrix'][0][0]
    bus_matrix = bus_matrix[:, 0:2, :]  # values p,q
    # bus_matrix = bus_matrix[:, 0:4, :]  # values p,q,v,theta
    line = data['data']['line'][0][0]
    line = line.astype(np.uint16)
    label = data['data']['label'][0][0]
    label = label.astype(np.uint16)

    g_list = []
    # 创建进度条
    #progress_bar = tqdm(total=100, desc='Importing model', unit='%', ncols=80)
    bar = progressbar.ProgressBar(max_value=bus_matrix.shape[2])
    bar.start()
    for i in range(bus_matrix.shape[2]):
        #progress_bar.update(1)
        bar.update(i+1)
        g = nx.Graph()
        for j in range(bus_matrix.shape[0]-1):
            g.add_node(j)
        for j in range(line.shape[0]-1):
            g.add_edge(line[j][0]-1, line[j][1]-1)
        node_features = bus_matrix[0:bus_matrix.shape[0]-1,:,i]
        g_list.append(S2VGraph(g, label[i].item(), list(np.zeros(bus_matrix.shape[0]-1)), node_features=node_features))
    g_list = add_labels_edge(g_list)
    print("")
    bar.finish()
    #progress_bar.close()
    ind_train_matrix = np.load('data/case39/ind_train_matrix.npy', allow_pickle=True)
    ind_test_matrix = np.load('data/case39/ind_test_matrix.npy', allow_pickle=True)

    train_graphs = [g_list[i] for i in ind_train_matrix[fold_idx,:]]
    test_graphs = [g_list[i] for i in ind_test_matrix[fold_idx,:]]
    train_label = label[ind_train_matrix[fold_idx, :], 0]
    test_label = label[ind_test_matrix[fold_idx, :], 0]

    return train_graphs, test_graphs, train_label, test_label

def loda_matdata_case2383(dataset, fold_idx):
    print('loading data')

    data = loadmat('data/case2383/case2383.mat')
    bus_matrix = data['data']['bus_matrix'][0][0]
    bus_matrix = bus_matrix[:, 0:2, :] # values p,q
    line = data['data']['line'][0][0]
    line = line.astype(np.int16)
    label = data['data']['label'][0][0]
    label = label.astype(np.int16)

    g_list = []
    ii = 0
    for i in range(bus_matrix.shape[2]):
        g = nx.Graph()
        for j in range(bus_matrix.shape[0]):
            g.add_node(j)
        for j in range(line.shape[0]-1):
            g.add_edge(line[j][0]-1, line[j][1]-1)
        node_features = bus_matrix[0:bus_matrix.shape[0],:,i]
        g_list.append(S2VGraph(g, label[i].item(), list(np.zeros(bus_matrix.shape[0])), node_features=node_features))
        ii += 1
        #print(ii)
    g_list = add_labels_edge(g_list)

    ind_train_matrix = np.load('data/case2383/ind_train_matrix.npy', allow_pickle=True)
    ind_test_matrix = np.load('data/case2383/ind_test_matrix.npy', allow_pickle=True)

    train_graphs = [g_list[i] for i in ind_train_matrix[fold_idx,:]]
    test_graphs = [g_list[i] for i in ind_test_matrix[fold_idx,:]]
    train_label = label[ind_train_matrix[fold_idx, :], 0]
    test_label = label[ind_test_matrix[fold_idx, :], 0]

    return train_graphs, test_graphs, train_label, test_label

def loda_matdata_case300(dataset, fold_idx):
    #print('loading data')
    print('开始导入电力系统数据...')
    bus_id = pd.read_csv('data/case300/bus.csv')
    line_id = pd.read_csv('data/case300/line.csv')
    # Read the CSV file into a DataFrame
    v_0 = pd.read_csv('data/case300/v_0.csv')
    list_i = []
    list_j = []
    bar = progressbar.ProgressBar(len(line_id))
    bar.start()
    for line_th in range(len(line_id)):
        bar.update(line_th+1)
        line_i = line_id.iloc[line_th]['I_No']
        line_j = line_id.iloc[line_th]['J_No']
        newline_i = np.where(v_0.iloc[:,1] == bus_id.iloc[line_i,1].strip().strip("'"))
        newline_j = np.where(v_0.iloc[:,1] == bus_id.iloc[line_j,1].strip().strip("'"))
        if newline_i[0].size == 0 or newline_j[0].size == 0:
            continue
        list_i.append(int(newline_i[0]))
        list_j.append(int(newline_i[0]))
    labels = pd.read_csv('data/case300/label.csv')['Istable']
    print("")
    bar.finish()
    label = []
    g_list = []
    for i in range(2000):
        g = nx.Graph()
        for j in range(v_0.shape[0]):
            g.add_node(j)
        for j in range(len(list_i)):
            g.add_edge(list_i[j], list_j[j])

        node_features = np.array(pd.read_csv('data/case300/v_'+str(i)+'.csv').iloc[:,2:10])
        node_features[np.isnan(node_features)] = 0

        if labels[i] == 1.0:
            tmp_label = 1
        else:
            tmp_label = 0
        label.append(tmp_label)
        g_list.append(S2VGraph(g, tmp_label, list(np.zeros(node_features.shape[0])), node_features=node_features))
    g_list = add_labels_edge(g_list)
    label = np.array(label)

    # 训练集和测试集划分
    # 比例是9:1
    ind_train_matrix = np.arange(0, 1800, 1)
    ind_test_matrix = np.arange(1800, 2000, 1)

    train_graphs = [g_list[i] for i in ind_train_matrix]
    test_graphs = [g_list[i] for i in ind_test_matrix]
    train_label = label[ind_train_matrix]
    test_label = label[ind_test_matrix]

    return train_graphs, test_graphs, train_label, test_label

def load_psdata(dataset, fold_idx):
    train_graphs, test_graphs, train_label, test_label =[],[],[],[]
    if dataset == 'CASE39':
        train_graphs, test_graphs, train_label, test_label = loda_matdata_case39(dataset, fold_idx)
    elif dataset == 'CASE2383':
        train_graphs, test_graphs, train_label, test_label = loda_matdata_case2383(dataset, fold_idx)
    elif dataset == 'CASE300':
        train_graphs, test_graphs, train_label, test_label = loda_matdata_case300(dataset, fold_idx)
    elif dataset == 'MIXED':
        train_graphs1, test_graphs1, train_label1, test_label1 = loda_matdata_case39(dataset, fold_idx)
        train_graphs2, test_graphs2, train_label2, test_label2 = loda_matdata_case2383(dataset, fold_idx)
        train_graphs.extend(train_graphs1)
        train_graphs.extend(train_graphs2)
        test_graphs.extend(test_graphs1)
        test_graphs.extend(test_graphs2)
        train_label = np.hstack((train_label1, train_label2))
        test_label = np.hstack((test_label1, test_label2))
    return train_graphs, test_graphs, train_label, test_label


