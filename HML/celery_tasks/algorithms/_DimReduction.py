from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from celery_tasks.algorithms._DimReduction_utils import gnn
from celery_tasks.algorithms._DimReduction_utils import c10folds

def algorithm_OneHot_train(data):
    model_enc = OneHotEncoder(sparse=False)
    model_enc.fit(data)
    data_onehot = pd.DataFrame(model_enc.transform(data))
    return data_onehot, model_enc


def algorithm_OneHot_apply(data, model_enc):
    data_onehot = pd.DataFrame(model_enc.transform(data))
    return data_onehot


def algorithm_PCA_train(data, n_components):
    model_pca = PCA(n_components=n_components)
    model_pca.fit(data)
    data_pca = pd.DataFrame(model_pca.transform(data))
    return data_pca, model_pca


def algorithm_PCA_apply(data, model_pca):
    data_pca = pd.DataFrame(model_pca.transform(data))
    return data_pca


def algorithm_GNN_train(data_path, n_components, epoch):
    c10folds.gen_data_from_mat(data_path)
    model_GNN = gnn.GNN(data_path,n_components, epoch)  # GNN is a shell of gnn
    model_gnn = model_GNN.main()
    data_GNN = pd.DataFrame( (model_GNN.Dim_Re(data_path,model_gnn)).numpy() )
    print("data_GNN=",data_GNN)
    return data_GNN, model_gnn

def algoritm_GNN_apply(data_path, model_GNN):
    data_GNN = pd.DataFrame(model_GNN.transform(data_path))
    return data_GNN

if __name__ == '__main__':
    algorithm_GNN_train("CASE39", 5, 3)