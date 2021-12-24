
from flask import current_app
import os
import numpy as np
import torch
import networkx as nx
import pandas as pd

from scipy.io import loadmat

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
    # np.random.shuffle(pos_id)
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
        print(ii)
    return g_list



def loda_matdata(fold_idx, datapath):
    print('loading data')
    import sys
    print(sys.argv[0])
    print(datapath)
    data = loadmat(datapath)
    bus_matrix = data['data']['bus_matrix'][0][0]
    bus_matrix = bus_matrix[:, 0:2, :]  # 只取 p,q 的值
    line = data['data']['line'][0][0]
    line = line.astype(np.uint16)
    label = data['data']['label'][0][0]
    label = label.astype(np.uint16)

    g_list = []
    for i in range(bus_matrix.shape[2]):
        g = nx.Graph()
        for j in range(bus_matrix.shape[0]-1):
            g.add_node(j)
        for j in range(line.shape[0]-1):
            g.add_edge(line[j][0]-1, line[j][1]-1)
        node_features = bus_matrix[0:bus_matrix.shape[0]-1,:,i]
        g_list.append(S2VGraph(g, label[i].item(), list(np.zeros(bus_matrix.shape[0]-1)), node_features=node_features))
    g_list = add_labels_edge(g_list)
    str1 = "ind_train_matrix.npy"
    str2 = "ind_test_matrix.npy"
#    str1 = os.path.join(current_app.config["SAVE_DATASET_PATH"],"ind_train_matrix.npy")
 #   str2 = os.path.join(current_app.config["SAVE_DATASET_PATH"],"ind_test_matrix.npy")
    ind_train_matrix = np.load(str1, allow_pickle=True)
    ind_test_matrix = np.load(str2, allow_pickle=True)

    train_graphs = [g_list[i] for i in ind_train_matrix[fold_idx,:]]
    test_graphs = [g_list[i] for i in ind_test_matrix[fold_idx,:]]
    train_label = label[ind_train_matrix[fold_idx, :], 0]
    test_label = label[ind_test_matrix[fold_idx, :], 0]

    return train_graphs, test_graphs, train_label, test_label



def load_psdata(fold_idx, datapath):
    train_graphs, test_graphs, train_label, test_label =[],[],[],[]
    train_graphs, test_graphs, train_label, test_label = loda_matdata(fold_idx, datapath)

    return train_graphs, test_graphs, train_label, test_label


