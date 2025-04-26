from mse import mse

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