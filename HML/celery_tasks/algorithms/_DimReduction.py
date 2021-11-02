from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import OneHotEncoder



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