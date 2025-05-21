import random

def mse(y):
    mean_y = sum(y) / len(y)
    return sum((yi - mean_y) ** 2 for yi in y) / len(y)

def best_split(X, y):
    n_samples, n_features = len(X), len(X[0])
    best_mse = float('inf')
    best_feature, best_threshold = None, None

    for feature_index in range(n_features):
        feature_values = [x[feature_index] for x in X]
        sorted_data = sorted(zip(feature_values, y, X), key=lambda tup: tup[0])

        for i in range(1, n_samples):
            if sorted_data[i-1][0] == sorted_data[i][0]:
                continue
            threshold = (sorted_data[i-1][0] + sorted_data[i][0]) / 2
            y_left = [tup[1] for tup in sorted_data[:i]]
            y_right = [tup[1] for tup in sorted_data[i:]]

            mse_left = mse(y_left)
            mse_right = mse(y_right)
            total_mse = len(y_left)/n_samples * mse_left + len(y_right)/n_samples * mse_right

            if total_mse < best_mse:
                best_mse = total_mse
                best_feature = feature_index
                best_threshold = threshold

    return best_feature, best_threshold

class RegressionTreeNode:
    def __init__(self, depth=0, max_depth=5, min_samples_split=2):
        self.depth = depth
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.left = None
        self.right = None
        self.feature_index = None
        self.threshold = None
        self.value = None

    def fit(self, X, y):
        if len(y) < self.min_samples_split or self.depth >= self.max_depth:
            self.value = sum(y) / len(y)
            return

        feature, threshold = best_split(X, y)
        if feature is None:
            self.value = sum(y) / len(y)
            return

        self.feature_index = feature
        self.threshold = threshold
        X_left, y_left, X_right, y_right = [], [], [], []

        for xi, yi in zip(X, y):
            if xi[feature] <= threshold:
                X_left.append(xi)
                y_left.append(yi)
            else:
                X_right.append(xi)
                y_right.append(yi)

        self.left = RegressionTreeNode(self.depth + 1, self.max_depth, self.min_samples_split)
        self.left.fit(X_left, y_left)
        self.right = RegressionTreeNode(self.depth + 1, self.max_depth, self.min_samples_split)
        self.right.fit(X_right, y_right)

    def predict(self, xi):
        if self.value is not None:
            return self.value
        if xi[self.feature_index] <= self.threshold:
            return self.left.predict(xi)
        else:
            return self.right.predict(xi)

class RandomForestRegressor:
    def __init__(self, n_estimators=10, max_depth=5, min_samples_split=2):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.trees = []

    def bootstrap_sample(self, X, y):
        n = len(X)
        indices = [random.randint(0, n - 1) for _ in range(n)]
        return [X[i] for i in indices], [y[i] for i in indices]

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_estimators):
            X_sample, y_sample = self.bootstrap_sample(X, y)
            tree = RegressionTreeNode(max_depth=self.max_depth, min_samples_split=self.min_samples_split)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

    def predict(self, X):
        predictions = []
        for xi in X:
            preds = [tree.predict(xi) for tree in self.trees]
            predictions.append(sum(preds) / len(preds))
        return predictions