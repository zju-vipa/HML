import pandas as pd
from celery_tasks.algorithms.learner_with_label_utils import gnn
from celery_tasks.algorithms.learner_with_label_utils import c10folds

def algorithm_GNN_train(data_path, n_components, epoch):
    c10folds.gen_data_from_mat(data_path)
    model_GNN = gnn.GNN(data_path = data_path,n_components = n_components, epoch = epoch, model = None)  # GNN is a shell of gnn
    model_gnn = model_GNN.main()
    #print("data_GNN=",data_GNN)
    return model_gnn