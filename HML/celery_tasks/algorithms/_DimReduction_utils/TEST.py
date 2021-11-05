from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
def main():
    data = np.array([[1., 1.],[0.9, 0.95],[1.01, 1.03],[2., 2.],
                  [2.03, 2.06],
                  [1.98, 1.89],
                  [3., 3.],
                  [3.03, 3.05],
                  [2.89, 3.1],
                  [4., 4.],
                  [4.06, 4.02],
                  [3.97, 4.01]])
    pca = PCA(n_components=2)
    newData = pd.DataFrame(pca.fit_transform(data))
    print(newData)
if __name__ == '__main__':
    main()