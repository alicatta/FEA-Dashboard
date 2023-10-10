import os
import pandas as pd

DATA_DIR = 'app/data'

def list_models():
    return os.listdir(DATA_DIR)

def load_model_data(model_name, location_name):
    file_path = os.path.join(DATA_DIR, model_name, f"{location_name}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

def list_locations(model_name):
    model_path = os.path.join(DATA_DIR, model_name)
    if os.path.exists(model_path):
        return [file.split('.csv')[0] for file in os.listdir(model_path)]
    return []
