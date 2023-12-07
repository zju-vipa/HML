import os
import pickle
import numpy as np
from tqdm import tqdm
import pandas as pd
import torch
from torch import nn
import torch.nn.functional as F

os.environ["DGLBACKEND"] = 'pytorch'
import dgl
from flask import current_app
from sklearn.preprocessing import StandardScaler
from celery_tasks.algorithms._FeatureEng_utils.factor.grid_dataset import GridDataset
from celery_tasks.algorithms._FeatureEng_utils.factor.factor_model import FactorGNN


class factorgnn(nn.Module):
    def __init__(self, data_path, result_path, lr=0.01, epoch=100, latent_dims=32, feat_drop=0, dis_weight=1):
        self.data_path = data_path
        self.num_layers = 4
        self.epoch = epoch
        self.latent_dims = latent_dims
        self.feat_drop = feat_drop
        self.dis_weight = dis_weight
        self.result_path = result_path
        self.lr = lr

    def main(self):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path, exist_ok=True)
        # 电网故障定位数据集
        dataset = GridDataset(self.data_path)
        dataloader = dgl.dataloading.GraphDataLoader(dataset, batch_size=64, shuffle=False, drop_last=True)
        # 每个branch文件可以构成一个图
        batched_graph_structure, _ = next(iter(dataloader))
        # 将图对象序列化并保存
        pickle.dump(dataset[0][0], open(os.path.join(self.result_path, 'graph_structure.pkl'), 'wb'))
        pickle.dump(pd.read_csv(os.path.join(self.data_path, 'line.csv')),
                    open(os.path.join(self.result_path, 'line.pkl'), 'wb'))
        batched_graph_structure = batched_graph_structure.to('cpu')
        self.in_feats = dataset[0][0].ndata['feat'].shape[1]
        self.hidden_feats = 32
        self.out_feats = 1
        # num_latent=4, feat_drop=0
        model = FactorGNN(batched_graph_structure, self.in_feats, self.hidden_feats, self.out_feats, self.num_layers,
                          self.feat_drop).to('cpu')
        criterion = nn.MSELoss()
        optimizer = torch.optim.AdamW(model.parameters(), self.lr)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, self.epoch)

        for epoch_id in range(self.epoch):
            (f'epoch: {epoch_id}')
            model.train()
            loss_array = []
            for (g, label) in tqdm(dataloader):
                g = g.to('cpu')
                label = label.to('cpu')
                optimizer.zero_grad()
                input = g.ndata['feat']
                h = model(input)
                h = h.reshape(64, -1, self.out_feats)
                h = h[:, 272, :].squeeze(-1)
                pred = F.sigmoid(h) * 100
                task_loss = criterion(pred, label)
                losses = model.compute_disentangle_loss()
                dis_loss = model.merge_loss(losses) * self.dis_weight
                loss = task_loss + dis_loss
                loss.backward()
                optimizer.step()
                loss_array.append(loss.detach().item())
            scheduler.step()
            print(f'avg mse loss: {np.array(loss_array).mean()}')
        torch.save(model.state_dict(), os.path.join(self.result_path, 'factor.pth'))
        model.load_state_dict(torch.load(os.path.join(self.result_path, 'factor.pth')))
        return model

    def feature_decoupling(self, model, data_path):
        model.eval()
        file_list = []
        feature_path = data_path
        for filename in tqdm(os.listdir(feature_path)):
            if filename.startswith('branch'):
                file_list.append(filename)
        graph_structure = pickle.load(open(os.path.join(self.result_path, 'graph_structure.pkl'), 'rb'))
        model = FactorGNN(graph_structure, self.in_feats, self.hidden_feats, self.out_feats, 4, 0)
        model.load_state_dict(torch.load(os.path.join(self.result_path, 'factor.pth')))
        line = pickle.load(open(os.path.join(self.result_path, 'line.pkl'), 'rb'))
        line = line.drop('ID_No', axis=1)
        nodes_num = len(line)
        edges_src = []
        edges_des = []
        for i in range(nodes_num):
            for j in range(i, nodes_num):
                u1, v1 = line['I_No'][i], line['J_No'][i]
                u2, v2 = line['I_No'][j], line['J_No'][j]
                if u1 == u2 or u1 == v2 or v1 == u2 or v1 == v2:
                    edges_src.append(i)
                    edges_des.append(j)
                    edges_src.append(j)
                    edges_des.append(i)
        edges_src = torch.LongTensor(edges_src)
        edges_des = torch.LongTensor(edges_des)
        feature_list = []
        pred_list = []
        with open(os.path.join(self.result_path, 'result.txt'), 'a', encoding='utf-8') as f:
            for filename in file_list:
                # 去除第二行及之后所有部分结尾有多余逗号的情况
                with open(os.path.join(feature_path, filename), 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                for i in range(1, len(lines)):
                    lines[i] = lines[i].rstrip('\n')
                    lines[i] = lines[i].strip(',')
                    lines[i] = lines[i] + '\n'
                with open(os.path.join(feature_path, filename), 'w', encoding='utf-8') as file:
                    file.writelines(lines)
                branch = pd.read_csv(os.path.join(feature_path, filename))
                branch = branch.rename(columns={'Unnamed: 0': 'IDName'})
                branch = branch.drop('ID_No', axis=1)
                branch.columns = branch.columns.str.strip()
                df = pd.merge(branch, line, how='inner', on=['IDName'])
                assert (df['IDName'].values == line['IDName'].values).all()
                assert df['IDName'][272] == 'AC32'
                edge_features = ['Qji(出J侧无功功率)', 'Ri(I侧视在电阻)', 'Qij(出I侧无功功率)', 'Zδi(I侧V/I夹角)',
                                 'Pji(出J侧有功功率)', \
                                 'δj(J侧母线电压相角)', 'δi(I侧母线电压相角)', 'Ij(J侧电流)', 'Vj(J侧母线幅值)',
                                 'Vi(I侧母线电压)', 'Xj(J侧视在电抗)', \
                                 'Zδj(J侧V/I夹角)', 'Ii(I侧电流)', 'Xi(I侧视在电抗)', 'ωi(I侧母线频率)',
                                 'Pij(出I侧有功功率)', 'ωj(J侧母线频率)', \
                                 'Rj(J侧视在电阻)']
                nodes_feat = df[edge_features].values
                scaler = StandardScaler()
                scaler.fit(nodes_feat)
                nodes_feat_scaled = scaler.transform(nodes_feat)
                nodes_feat_scaled = torch.FloatTensor(nodes_feat_scaled)
                g = dgl.graph((edges_src, edges_des))
                g.ndata['feat'] = nodes_feat_scaled
                with torch.no_grad():
                    # # 存解耦层特征
                    # input = g.ndata['feat']
                    # h = model(input).detach()
                    # feature = model.feat_list[-1].detach().numpy()
                    # feature_list.append(feature)

                    # 存最后一层特征
                    input = g.ndata['feat']
                    h = model(input)
                    h_temp = []
                    for h_i in h:
                        h_temp.append(h_i.item())
                    feature_list.append(h_temp)
                    h = h.reshape(-1, self.out_feats)
                    h = h[272, :].squeeze(-1)
                    pred = torch.round(F.sigmoid(h) * 100)
                    pred_lo = max(2, int(pred.item()) - 5)
                    pred_hi = min(98, int(pred.item()) + 5)
                    f.write(f'{filename[:-4]:<12} - {pred_lo:>2}%~{pred_hi:>2}%\n')

        feature_list = np.array(feature_list)
        columns = ['factorgnn_{}'.format(j) for j in range(feature_list.shape[1])]
        feature = pd.DataFrame(feature_list, columns=columns)
        labels = pd.read_csv(os.path.join(data_path, 'label.csv'))
        labels.sort_values(by=labels.columns[0], key=lambda x: x.map(str))
        feature['label'] = labels['K%'].astype(np.float32)

        # 总的预测准确率
        result_list = (labels['K%'] - pd.Series(pred_list)).tolist()
        count = np.sum(np.abs(result_list) <= 5)
        length = len(result_list)
        accuracy = count / length
        print('预测准确率为：', accuracy)
        return feature