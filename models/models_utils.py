import joblib
from models.full_code import RandomForestRegressor, RegressionTreeNode, best_split, mse

# Load mô hình từ file
def load_model(path):
    with open(path, 'rb') as f:
        model = joblib.load(f)
    return model

# Hàm dự đoán
def predict(model, input_data, type="day"):
    return model[type].predict(input_data)