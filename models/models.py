import pickle

# Mô hình RandomForestRegressor
from RandomForestRegressor import RandomForestRegressor
from RegressionTreeNode import RegressionTreeNode
from best_split import best_split
from mse import mse

# Đọc file pickle
with open('models/models.pkl', 'rb') as f:
    models = pickle.load(f)

# Kiểm tra kiểu dữ liệu
print(type(models))

# Nếu là dict hoặc list, có thể in thử nội dung
print(models)