from utils.ctgan_new.ctgan_model import CTGANSynthesizer
from flask import current_app
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import torch
import torch.nn as nn
# torch.manual_seed(1)  # Set seed for reproducibility.

ctgan_path = os.path.join(current_app.config["ROOT_PATH"], 'utils')
sys.path.append(ctgan_path)

def ctgan_data_generation_c(file_path=None, n_sample=10,
                            cond_stability=0, cond_load=0.0):
    model_name = 'ctgan_psat_dataset_data3_train_1600vs1600_epoch3000_b500_d1_g1'
    model_path = os.path.join(current_app.config["ROOT_PATH"], 'utils', 'model',
                 model_name + '.pkl')
    model = CTGANSynthesizer.load(model_path)
    # model = CTGAN.load('result/model/ctgan_%s_epoch%d.pkl' % (dataset_name, epochs))
    # Synthetic copy
    # samples = model.sample(n=1000, condition_column='convergency', condition_value='1')
    if cond_stability > 0:
        samples = model.sample(n=n_sample, condition_column='stability', condition_value=cond_stability)
        samples.to_csv(file_path, header=True, index=False)
        return 1
    elif cond_load > 0:
        samples = model.sample(n=n_sample, condition_column='load_setting', condition_value=cond_load)
        samples.to_csv(file_path, header=True, index=False)
        return 2
    else:
        samples = model.sample(n=n_sample)
        samples.to_csv(file_path, header=True, index=False)
        return 3



def Block(in_channels, out_channels):
    return nn.Sequential(
        nn.Linear(in_channels, out_channels),
        nn.BatchNorm1d(out_channels),
        # nn.Dropout(0.1),
        nn.ReLU(),)

class TabelNet(nn.Module):
    def __init__(self):
        super().__init__()
        # self.pre = nn.BatchNorm1d(200)
        self.pre = nn.BatchNorm1d(180)

        self.cls = nn.Sequential(
            Block(180, 128),
            Block(128, 64),
            Block(64, 32),
            Block(32, 2),)

    def forward(self, x):
        x = self.pre(x)
        return self.cls(x)


def ctgan_data_train_tablenet_loss(file_path=None):
    if file_path is None:
        return 'file_path is None'
    # read the ctgan dataset
    data_train_pd = pd.read_csv(file_path+'.csv')
    # Convert features and labels to numpy arrays.
    # 原：1暂态稳定，2暂态失稳；减1之后：0暂态稳定，1暂态失稳
    train_labels = data_train_pd['stability'].to_numpy() - 1
    label_tensor = torch.from_numpy(train_labels)
    train_data = data_train_pd.drop(['stability', 'load_setting'], axis=1)
    train_data = train_data.to_numpy()
    train_data_tensor = torch.from_numpy(train_data).type(torch.FloatTensor)
    # train TableNet
    max_epoch = 100
    net = TabelNet()
    crition = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(net.parameters(), lr=1e-3, weight_decay=5e-4, eps=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer,
                                                           T_max=max_epoch,
                                                           eta_min=0)
    Loss = []
    net.train()
    for epoch in range(max_epoch):
        output = net(train_data_tensor)
        loss = crition(input=output, target=label_tensor)
        running_loss = loss.item()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()
        if epoch % 1 == 0:
            print('Epoch {}/{} => Loss: {:.3f}'.format(epoch + 1, max_epoch, loss.item()))
            Loss.append(running_loss)
    y = np.array(Loss)
    np.save(file_path+'_loss_save', y)
    # enc = np.load('result/test/tablenet_loss_epoch_{}.npy'.format(n))
    # y = list(enc)
    x = range(0, len(y))
    plt.plot(x, y, '.-')
    plt_title = 'loss vs epoch'
    plt.title(plt_title)
    plt.xlabel('epoch')
    plt.ylabel('loss')
    file_name_fig = file_path+'_loss_vs_epoch.jpg'
    plt.savefig(file_name_fig)
    plt.close()
    return file_name_fig
