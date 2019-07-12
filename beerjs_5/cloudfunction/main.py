import pandas as pd
import pandas_gbq as pbq
import logging
from utils import download_file_from_storage
import xgboost as xgb
import dill as pickle

PROJECT_ID = "gcp-projec"
DESTINATION_DATASET = "dataset_name"
DESTINATION_TABLE = "dataset_table"

def predict_new_file(data, context):
    bucket_name = format(data['bucket'])
    storage_file = format(data['name'])

    local_file = download_file_from_storage(bucket_name, storage_file)
    
    data = pd.read_csv(local_file)
    
    predict_data = pd.get_dummies(data)
    
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    
    data['predicted_value'] =  model.predict(predict_data)

    pbq.to_gbq(dataframe=data,
              if_exists="append",
              project_id=PROJECT_ID,
              destination_table="{0}.{1}".format(DESTINATION_DATASET, DESTINATION_TABLE))