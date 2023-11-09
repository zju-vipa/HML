import numpy as np

class Node:
    def __init__(self, feature_index=None, threshold=None, value=None, left=None, right=None):
        self.feature_index = feature_index # 特征索引
        self.threshold = threshold # 分割阈值
        self.value = value # 叶子节点的值
        self.left = left # 左子节点
        self.right = right # 右子节点

class DecisionTreeClassifier:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth

    def fit(self, X, y):
        self.n_classes_ = len(set(y))
        self.n_features_ = X.shape[1]
        self.tree_ = self._build_tree(X, y)

    def _build_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_labels = len(set(y))

        # 终止条件
        if depth == self.max_depth or n_labels == 1 or n_samples <= 1:
            return Node(value=self._most_common_label(y))

        # 选择最佳分割特征和阈值
        best_feature, best_threshold = self._find_best_split(X, y)

        # 划分数据集
        left_indices = np.where(X[:, best_feature] <= best_threshold)[0]
        right_indices = np.where(X[:, best_feature] > best_threshold)[0]

        # 递归构建左右子树
        left = self._build_tree(X[left_indices], y[left_indices], depth + 1)
        right = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        # 创建节点
        return Node(feature_index=best_feature, threshold=best_threshold, left=left, right=right)

    def _find_best_split(self, X, y):
        best_gain = -1
        best_feature = None
        best_threshold = None

        for feature in range(self.n_features_):
            unique_values = np.unique(X[:, feature])
            thresholds = (unique_values[:-1] + unique_values[1:]) / 2

        for threshold in thresholds:
            gain = self._information_gain(X, y, feature, threshold)

            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_threshold = threshold

        return best_feature, best_threshold

    def _information_gain(self, X, y, feature, threshold):
        parent_entropy = self._entropy(y)
        left_indices = np.where(X[:, feature] <= threshold)[0]
        right_indices = np.where(X[:, feature] > threshold)[0]
        left_entropy = self._entropy(y[left_indices])
        right_entropy = self._entropy(y[right_indices])
        n = len(y)
        left_ratio = len(left_indices) / n
        right_ratio = len(right_indices) / n

        gain = parent_entropy - (left_ratio * left_entropy + right_ratio * right_entropy)
        return gain

    def _entropy(self, y):
        _, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return entropy

    def _most_common_label(self, y):
        labels, counts = np.unique(y, return_counts=True)
        index = np.argmax(counts)
        return labels[index]

    def predict(self, X):
        return [self._traverse_tree(x, self.tree_) for x in X]

    def _traverse_tree(self, x, node):
        if node.value is not None:
            return node.value

        if x[node.feature_index] <= node.threshold:
            return self._traverse_tree(x, node.left)
        else:
            return self._traverse_tree(x, node.right)
            return self._traverse_tree(x, node.right)