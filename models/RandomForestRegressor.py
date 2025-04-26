from RegressionTreeNode import RegressionTreeNode
import random

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