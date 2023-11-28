import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import torch
os.environ["DGLBACKEND"] = 'pytorch'
import dgl
from dgl.data import DGLDataset
from tqdm import tqdm

class GridDataset(DGLDataset):
    def __init__(self, data_path):
        self.data_path = data_path
        super().__init__(name='grid dataset')

    def process(self):
        self.path = self.data_path
        self.bus = pd.read_csv(os.path.join(self.data_path, 'bus.csv'))
        self.line = pd.read_csv(os.path.join(self.data_path, 'line.csv'))
        self.label = pd.read_csv(os.path.join(self.path, 'label.csv'))
        file_list = []
        for filename in tqdm(os.listdir(self.path)):
            if filename.startswith('branch'):
                file_list.append(filename)
        self.len = len(file_list)
        self.line = self.line.drop('ID_No', axis=1)
        self.label['K%'] = self.label['K%']
        self.label = torch.FloatTensor(self.label['K%'].astype(np.float32))

        # 将原图转化为line graph的形式
        # https://en.wikipedia.org/wiki/Line_graph
        # 线图：反映图中的边的连接关系
        # 将线路转换为节点
        # 将线路之间的相邻关系转换为边
        nodes_num = len(self.line)
        self.edges_src = []
        self.edges_des = []

        for i in range(nodes_num):
            for j in range(i, nodes_num):
                u1, v1 = self.line['I_No'][i], self.line['J_No'][i]
                u2, v2 = self.line['I_No'][j], self.line['J_No'][j]

                if u1 == u2 or u1 == v2 or v1 == u2 or v1 == v2:
                    self.edges_src.append(i)
                    self.edges_des.append(j)

                    self.edges_src.append(j)
                    self.edges_des.append(i)

        self.edges_src = torch.LongTensor(self.edges_src)
        self.edges_des = torch.LongTensor(self.edges_des)

    def __getitem__(self, i):
        branch_i_path = f'{self.path}/branch_{i}.csv'
        branch_i = pd.read_csv(branch_i_path)
        branch_i = branch_i.rename(columns={'Unnamed: 0': 'IDName'})
        branch_i = branch_i.drop('ID_No', axis=1)

        df = pd.merge(branch_i, self.line, how='inner', on=['IDName'])

        assert (df['IDName'].values == self.line['IDName'].values).all()
        assert df['IDName'][272] == 'AC32'

        edge_features = ['Qji(出J侧无功功率)', 'Ri(I侧视在电阻)', 'Qij(出I侧无功功率)', 'Zδi(I侧V/I夹角)', 'Pji(出J侧有功功率)', 'δj(J侧母线电压相角)', 'δi(I侧母线电压相角)', 'Ij(J侧电流)', 'Vj(J侧母线幅值)', 'Vi(I侧母线电压)', 'Xj(J侧视在电抗)', 'Zδj(J侧V/I夹角)', 'Ii(I侧电流)', 'Xi(I侧视在电抗)', 'ωi(I侧母线频率)', 'Pij(出I侧有功功率)', 'ωj(J侧母线频率)', 'Rj(J侧视在电阻)']
        # 节点特征归一化
        nodes_feat = df[edge_features].values
        scaler = StandardScaler()
        scaler.fit(nodes_feat)
        nodes_feat_scaled = scaler.transform(nodes_feat)
        nodes_feat_scaled = torch.FloatTensor(nodes_feat_scaled)
        # 生成dgl图
        g = dgl.graph((self.edges_src, self.edges_des))
        g.ndata['feat'] = nodes_feat_scaled
        # label是文件中K%这项
        return g, self.label[i]

    def __len__(self):
        return self.len