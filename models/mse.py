def mse(y):
    mean_y = sum(y) / len(y)
    return sum((yi - mean_y) ** 2 for yi in y) / len(y)