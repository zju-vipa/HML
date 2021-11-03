from utils.ctgan_new.ctgan_model import CTGANSynthesizer
from flask import current_app
import os
import sys

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
