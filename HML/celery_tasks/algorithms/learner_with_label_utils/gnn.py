


# coding=utf-8

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from tqdm import tqdm
from scipy.io import loadmat
from celery_tasks.algorithms._DimReduction_utils.gcpool.util import separate_data
from celery_tasks.algorithms._DimReduction_utils.gcpool.util import load_psdata
# from models.graphcnn import GraphCNN
# from sopool_attn.graphcnn import GraphCNN
from celery_tasks.algorithms._DimReduction_utils.gcpool.graphcnn import GraphCNN

criterion = nn.CrossEntropyLoss()
class GNN():
    def __init__(self, datapath="CASE39", n_component=10, epoch = 100 ,model=None):
        self.datapath = datapath
        self.n_component = n_component
        self.epoch = epoch
        self.model = model
    def performance(self, predicted, expected):
        predicted = np.array(predicted.cpu(), dtype='uint8').squeeze(1)
        res = (predicted ^ expected)  # 亦或使得判断正确的为0,判断错误的为1
        r = np.bincount(res)
        tp_list = ((predicted) & (expected))
        fp_list = (predicted & (~expected))
        tp_list = tp_list.tolist()
        fp_list = fp_list.tolist()
        tp = tp_list.count(1)
        fp = fp_list.count(1)
        tn = r[0] - tp
        fn = (len(res) - r[0]) - fp
        tnr = tn / (tn + fp)
        tpr = tp / (tp + fn)
        F1 = (2 * tp) / (2 * tp + fn + fp)
        acc = (tp + tn) / (tp + tn + fp + fn)
        # recall = tp / (tp + fn)
        return F1, acc, tnr, tpr

    def train(self, args, device, train_graphs, optimizer, epoch):
        self.model.train()

        total_iters = args.iters_per_epoch
        pbar = tqdm(range(total_iters), unit='batch')

        loss_accum = 0
        for pos in pbar:
            selected_idx = np.random.permutation(len(train_graphs))[:args.batch_size]

            batch_graph = [train_graphs[idx] for idx in selected_idx]
            output = self.model(batch_graph)

            labels = torch.LongTensor([graph.label for graph in batch_graph]).to(device)

            # compute loss
            loss = criterion(output, labels)

            # backprop
            if optimizer is not None:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            loss = loss.detach().cpu().numpy()
            loss_accum += loss

            # report
            pbar.set_description('epoch: %d' % (epoch))

        average_loss = loss_accum / total_iters
        print("loss training: %f" % (average_loss))

        return average_loss

    ###pass data to model with minibatch during testing to avoid memory overflow (does not perform backpropagation)
    def pass_data_iteratively(self, graphs, minibatch_size=64):
        self.model.eval()
        output = []
        idx = np.arange(len(graphs))
        for i in range(0, len(graphs), minibatch_size):
            sampled_idx = idx[i:i + minibatch_size]
            if len(sampled_idx) == 0:
                continue
            output.append(self.model([graphs[j] for j in sampled_idx]).detach())
        #print("output=",output)
        return torch.cat(output, 0)

    def Test(self, args, device, train_graphs, test_graphs, epoch):
        self.model.eval()

        # output = pass_data_iteratively(model, train_graphs)
        # pred = output.max(1, keepdim=True)[1]
        # labels = torch.LongTensor([graph.label for graph in train_graphs]).to(device)
        # correct = pred.eq(labels.view_as(pred)).sum().cpu().item()
        # acc_train = correct / float(len(train_graphs))

        output = self.pass_data_iteratively(test_graphs)
        pred = output.max(1, keepdim=True)[1]
        labels = torch.LongTensor([graph.label for graph in test_graphs]).to(device)
        correct = pred.eq(labels.view_as(pred)).sum().cpu().item()
        acc_test = correct / float(len(test_graphs))
        # print("accuracy train: %f test: %f" % (acc_train, acc_test))
        #
        # return acc_train, acc_test
        return acc_test, pred

    def Dim_Re(self,datapath):
        self.model.eval()
        self.model.Is_dim = True
        # output = pass_data_iteratively(model, train_graphs)
        # pred = output.max(1, keepdim=True)[1]
        # labels = torch.LongTensor([graph.label for graph in train_graphs]).to(device)
        # correct = pred.eq(labels.view_as(pred)).sum().cpu().item()
        # acc_train = correct / float(len(train_graphs))
        train_graphs, test_graphs, train_label, test_label = load_psdata(0, datapath)
        input=train_graphs+test_graphs
        output = self.pass_data_iteratively(input)
        self.model.Is_dim = False
        #print("output=",output)
        return output   # need pd.dataframe
    def main(self):
        # Training settings
        # Note: Hyper-parameters need to be tuned in order to obtain results reported in the paper.
        #parser = argparse.ArgumentParser(
        #    description='PyTorch graph convolutional neural net for whole-graph classification')
        class Parser():
            def __init__(self, n_component, epoch):
                self.device = 0
                self.batch_size = 32
                self.iters_per_epoch = 50
                self.epochs = epoch
                self.lr = 0.001
                self.seed = 0
                self.fold_idx = 0
                self.num_layers = 5
                self.num_mlp_layers = 2
                self.hidden_dim = 32
                self.final_dropout = 0.5
                self.graph_pooling_type = "sum"
                self.neighbor_pooling_type = "sum"
                self.fac_dim = 1
                self.rep_dim = n_component
                self.fo_type = 0
                self.so_type = 0
                self.train_ratio = 0.9
                self.learn_eps = False

        args = Parser(self.n_component, self.epoch)

        # set up seeds and gpu device
        torch.manual_seed(0)
        np.random.seed(0)
        torch.set_num_threads(10)  # 设置CPU占用核数
        num_classes = 2

        device = torch.device("cuda:" + str(args.device)) if torch.cuda.is_available() else torch.device("cpu")
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(0)

        train_graphs, test_graphs, train_label, test_label = load_psdata(args.fold_idx, self.datapath)
        self.model = GraphCNN(args.num_layers, args.num_mlp_layers, train_graphs[0].node_features.shape[1], args.hidden_dim,
                         num_classes,
                         args.fac_dim, args.rep_dim, args.final_dropout, args.learn_eps, args.graph_pooling_type,
                         args.neighbor_pooling_type,
                         args.fo_type, args.so_type, device).to(device)

        optimizer = optim.Adam(self.model.parameters(), lr=args.lr)


        path_ = 'GNN'+str(args.fo_type) + '_' + str(args.fold_idx) + '_' + str(
             args.batch_size) + '_' + str(args.hidden_dim) + '_' + str(args.lr) + '_.pth'
        max_acc = 0.0
        max_F1 = 0.0
        max_tnr = 0.0
        max_tpr = 0.0
        max_state_dict = self.model.state_dict()
        for epoch in range(1, args.epochs + 1):

            avg_loss = self.train(args, device, train_graphs, optimizer, epoch)
            acc_test, pred_test = self.Test(args, device, train_graphs, test_graphs, epoch)
            optimizer.step()
            # print(model.state_dict())
            F1, acc, tnr, tpr = self.performance(pred_test, test_label)
            if acc > max_acc:
                max_acc = acc
                max_F1 = F1
                max_tnr = tnr
                max_tpr = tpr
                max_state_dict = self.model.state_dict()

            print("performance F1, acc, tnr, tpr : %f %f %f %f" % (max_acc, max_F1, max_tnr, max_tpr))
            print("")
        torch.save(max_state_dict, path_)
        self.model.load_state_dict(torch.load(path_))
        return self.model
if __name__ == '__main__':
    tmp= GNN()
    tmp.main()