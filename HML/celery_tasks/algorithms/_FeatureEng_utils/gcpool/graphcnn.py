# coding=utf-8
import argparse
import os.path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from tqdm import tqdm
from celery_tasks.algorithms._FeatureEng_utils.gcpool.utils import load_psdata
from celery_tasks.algorithms._FeatureEng_utils.gcpool.graph_model import GraphCNN
from flask import current_app

criterion = nn.CrossEntropyLoss()


class graphcnn():
    def __init__(self, datapath, result_path, num_layers=5, n_components=10, epoch=100):
        self.datapath = datapath
        self.result_path = result_path
        self.num_layers = num_layers
        self.n_component = n_components
        self.epoch = epoch

    def performance(self, predicted, expected):
        predicted = np.array(predicted.cpu(), dtype='uint8').squeeze(1)
        res = (predicted ^ expected)
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

    def train(self, args, model, device, train_graphs, optimizer, epoch):
        model.train()
        total_iters = args.iters_per_epoch
        pbar = tqdm(range(total_iters), unit='batch')
        loss_accum = 0
        for pos in pbar:
            selected_idx = np.random.permutation(len(train_graphs))[:args.batch_size]
            batch_graph = [train_graphs[idx] for idx in selected_idx]
            output = model(batch_graph)
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
    def pass_data_iteratively(self, model, graphs, minibatch_size=64):
        model.eval()
        output = []
        idx = np.arange(len(graphs))
        for i in range(0, len(graphs), minibatch_size):
            sampled_idx = idx[i:i + minibatch_size]
            if len(sampled_idx) == 0:
                continue
            output.append(model([graphs[j] for j in sampled_idx]).detach())
        return torch.cat(output, 0)

    def test(self, args, model, device, train_graphs, test_graphs, epoch):
        model.eval()
        output = self.pass_data_iteratively(model, test_graphs)
        pred = output.max(1, keepdim=True)[1]
        labels = torch.LongTensor([graph.label for graph in test_graphs]).to(device)
        correct = pred.eq(labels.view_as(pred)).sum().cpu().item()
        acc_test = correct / float(len(test_graphs))
        return acc_test, pred

    def Dim_Re(self, model, datapath):
        model.eval()
        model.Is_dim = True
        train_graphs, test_graphs, train_label, test_label = load_psdata(datapath, 'CASE300', 0)
        input = train_graphs + test_graphs
        output = self.pass_data_iteratively(model, input).cpu().numpy()
        model.Is_dim = False
        return output  # need pd.dataframe

    def main(self):
        class Parser():
            def __init__(self, num_layers, n_components, epoch):
                self.dataset = 'CASE300'
                self.device = 0
                self.batch_size = 32
                self.iters_per_epoch = 50
                self.epochs = epoch
                self.lr = 0.001
                self.seed = 0
                self.fold_idx = 0
                self.num_layers = num_layers
                self.num_mlp_layers = 2
                self.hidden_dim = 32
                self.final_dropout = 0.5
                self.graph_pooling_type = "sum"
                self.neighbor_pooling_type = "sum"
                self.fac_dim = 1
                self.rep_dim = n_components
                self.filename = "10flod.txt"
                self.fo_type = 0
                self.so_type = 0
                self.train_ratio = 0.9
                self.learn_eps = False

        args = Parser(self.num_layers, self.n_component, self.epoch)

        # set up seeds and gpu device
        torch.manual_seed(0)
        np.random.seed(0)
        torch.set_num_threads(10)
        device = torch.device("cuda:" + str(args.device)) if torch.cuda.is_available() else torch.device("cpu")
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(0)

        num_classes = 2

        train_graphs, test_graphs, train_label, test_label = load_psdata(self.datapath, args.dataset, args.fold_idx)
        model = GraphCNN(args.num_layers, args.num_mlp_layers, train_graphs[0].node_features.shape[1], args.hidden_dim,
                         num_classes,
                         args.fac_dim, args.rep_dim, args.final_dropout, args.learn_eps, args.graph_pooling_type,
                         args.neighbor_pooling_type,
                         args.fo_type, args.so_type, device).to(device)

        optimizer = optim.Adam(model.parameters(), lr=args.lr)
        # 暂时先写这个
        save_path = self.result_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        path_ = save_path + '/' + str(args.dataset) + '_' + str(args.fold_idx) + '_' + str(args.batch_size) + '_' + str(
            args.hidden_dim) + '_' + str(args.lr) + '_.pth'

        max_acc = 0.0
        max_F1 = 0.0
        max_tnr = 0.0
        max_tpr = 0.0
        max_state_dict = model.state_dict()
        for epoch in range(1, args.epochs + 1):
            avg_loss = self.train(args, model, device, train_graphs, optimizer, epoch)
            acc_test, pred_test = self.test(args, model, device, train_graphs, test_graphs, epoch)
            optimizer.step()
            F1, acc, tnr, tpr = self.performance(pred_test, test_label)
            if acc > max_acc:
                max_acc = acc
                max_F1 = F1
                max_tnr = tnr
                max_tpr = tpr
                max_state_dict = model.state_dict()
                # max_model = GraphCNN(args.num_layers, args.num_mlp_layers, train_graphs[0].node_features.shape[1],
                #                  args.hidden_dim, num_classes,
                #                  args.fac_dim, args.rep_dim, args.final_dropout, args.learn_eps, args.graph_pooling_type,
                #                  args.neighbor_pooling_type,
                #                  args.fo_type, args.so_type, device).to(device)
                # max_model.load_state_dict(max_state_dict)

            current_app.logger.info("performance F1, acc, tnr, tpr : %f %f %f %f" % (max_F1, max_acc, max_tnr, max_tpr))

        torch.save(max_state_dict, path_)
        model.load_state_dict(torch.load(path_))
        return model
        # with open(str('result/')+str(args.dataset)+'_' + 'F1' + '_'+ str(args.batch_size) + '_'+ str(args.hidden_dim) + '_'+  str(args.epochs)+'_' + str(args.lr)+ '_results.txt', 'a+') as f:
        #     f.write(str(max_F1) + '\n')
        # with open(str('result/')+str(args.dataset)+'_' + 'ACC' + '_'+ str(args.batch_size) + '_'+ str(args.hidden_dim) + '_'+ str(args.epochs)+'_' + str(args.lr)+ '_results.txt', 'a+') as f:
        #     f.write(str(max_acc) + '\n')
        # with open(str('result/')+str(args.dataset)+'_' + 'TNR' + '_'+ str(args.batch_size) + '_'+ str(args.hidden_dim) + '_'+ str(args.epochs)+'_' + str(args.lr)+ '_results.txt', 'a+') as f:
        #     f.write(str(max_tnr) + '\n')
        # with open(str('result/')+str(args.dataset)+'_' + 'TPR' + '_'+ str(args.batch_size) + '_'+ str(args.hidden_dim) + '_'+ str(args.epochs)+'_' + str(args.lr)+ '_results.txt', 'a+') as f:
        #     f.write(str(max_tpr) + '\n')


if __name__ == '__main__':
    gnn = graphcnn()
    gnn.main()