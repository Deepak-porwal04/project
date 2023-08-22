file_path = # data file path and name
from sensor.data_access.sensor_data import SensorData
from sensor.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from main import set_env_variable
import os

if __name__=='__main__':
    data_file_path = # data file path should be available in project folder
    env_file_path = # env.yaml file path should be available in project folder
    set_env_variable(env_file_path)
    print(os.environ['MONGO_DB_URL'])
    sd = SensorData()
    if DATA_INGESTION_COLLECTION_NAME in sd.mongo_client.database.list_collection_names():
        sd.mongo_client.database[DATA_INGESTION_COLLECTION_NAME].drop()
    sd.save_csv_file(file_path=data_file_path, collection_name=DATA_INGESTION_COLLECTION_NAME)