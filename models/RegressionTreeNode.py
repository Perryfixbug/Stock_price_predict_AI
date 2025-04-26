from best_split import best_split

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