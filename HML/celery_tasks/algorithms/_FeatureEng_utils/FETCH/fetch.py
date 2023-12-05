import argparse
import os.path

import pandas as pd
import warnings

from celery_tasks.algorithms._FeatureEng_utils.FETCH.autofe import AutoFE

warnings.filterwarnings("ignore")

class Parser():
    def __init__(self, steps_num, worker, epoch):
        self.cuda = "0"
        self.train_size = 0.7
        self.epochs = epoch
        self.ppo_epochs = 10
        self.episodes = 24
        self.lr = 1e-4
        self.entropy_weight = 1e-4
        self.baseline_weight = 0.95
        self.gama = 0.9
        self.gae_lambda = 0.95
        self.batch_size = 64
        self.d_model = 128
        self.d_k = 32
        self.d_v = 32
        self.d_ff = 64
        self.n_heads = 6
        self.worker = worker
        self.steps_num = steps_num
        self.combine = True
        self.preprocess = False
        self.seed = 1
        self.cv = 5
        self.cv_train_size = 0.7
        self.cv_seed = 1
        self.split_train_test = False
        self.shuffle = False
        self.enc_c_pth = ''
        self.enc_d_pth = ''
        self.mode = None
        self.model = 'rf'
        self.metric = None
        self.file_name = 'grid'

class fetch():
    def __init__(self, result_path, steps_num=3, worker=12, epoch=100):
        self.result_path = result_path
        self.steps_num = steps_num
        self.worker = worker
        self.epoch = epoch

    def main(self, data):
        args = Parser(self.steps_num, self.worker, self.epoch)
        configs = {'mode': 'regression',
                   'c_columns': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
                                 '15', '16'],
                   'd_columns': [],
                   'target': 'label',
                   "model": "lgb",
                   "dataset_path": "data/grid.csv",
                   "metric": "grid_score"}
        data_configs = configs
        c_columns = data_configs['c_columns']
        d_columns = data_configs['d_columns']
        target = data_configs['target']
        mode = data_configs['mode']
        model = data_configs["model"]
        if args.metric:
            metric = args.metric
        else:
            metric = data_configs["metric"]

        args.mode = mode
        args.model = model
        args.metric = metric
        args.c_columns = c_columns
        args.d_columns = d_columns
        args.target = target
        df = data
        df_part = pd.DataFrame()
        sample_interval = 20
        columns = df.columns.tolist()
        df_out_col = len(df.columns)
        # 得到5000x?维的部分特征
        for i in range(0, df_out_col - 1, sample_interval):
            j = i / sample_interval
            df_part[f'{int(j)}'] = df[columns[i]]
        df_part['label'] = df['label']
        df_part.to_csv(self.result_path, index=False)
        df_part = pd.read_csv(self.result_path)
        autofe = AutoFE(df_part, args)
        data = autofe.fit_attention(args)
        data['label'] = df['label']
        return data, autofe

if __name__ == '__main__':
    machine = fetch.fetch('celery_tasks/algorithms/_FeatureEng_utils/FETCH/data','celery_tasks/algorithms/_FeatureEng_utils/FETCH/result', steps_num=1, worker=5, epoch=1)
    data, model = machine.main()
    data_factor = len(data)
    print(data_factor)

