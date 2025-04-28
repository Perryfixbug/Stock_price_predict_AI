import pickle

# Mô hình RandomForestRegressor
from models.RandomForestRegressor import RandomForestRegressor
from models.RegressionTreeNode import RegressionTreeNode
from models.best_split import best_split
from models.mse import mse

# Đọc file pickle
with open('models/models.pkl', 'rb') as f:
    models = pickle.load(f)

# Kiểm tra kiểu dữ liệu
print(type(models))

# Nếu là dict hoặc list, có thể in thử nội dung
print(models)

def predict(input_data, type='day'):
    # Dự đoán bằng mô hình đã tải
    predictions = models[type].predict(input_data)
    return predictions