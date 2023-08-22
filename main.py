from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.utils.main_utils import read_yaml_file, load_object
from sensor.logger import logging
from sensor.pipeline.training_pipeline import TrainPipeline

from fastapi import FastAPI
from sensor.constant.application import APP_HOST,APP_PORT
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

def set_env_variable(env_file_path):
    env_config = read_yaml_file(env_file_path)
    os.environ['MONGO_DB_URL']= env_config['MONGO_DB_URL']

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

env_file_path = 'env.yaml'
# set_env_variable(env_file_path)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running")
        train_pipeline.run_pipeline()
        return Response("Training Successful")
    except Exception as e:
        return Response(f"Error Occured {e} !!")
    
@app.get("/predict")
async def predict_route():
    try:
        """
        use ModelResolver(), load_object and SAVED_MODEL_DIR and edit this docstring
        """
        # get data from user as csv file
        # convert csv to df
        df = None
        # cn upload train df
        # can calculate dataa drift if it is significant then trigger the training
        # otherwise trigger a email to data science team, data drift detected
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")
        best_model_path = model_resolver.get_best_model_path
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df["predicted_column"] = y_pred
        df["predicted_column"].replace(TargetValueMapping().reverse_mapping(),inplace=True)
        # decide how to return file to user
    except Exception as e:
        raise Response(f"Error occured {e}")
    

    

def main():
    try:
        env_file_path = 'env.yaml'# path of env.yaml file cntaining env variables
        set_env_variable(env_file_path) 
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    try:
        # main()
        set_env_variable(env_file_path)
        app_run(app, host=APP_HOST, port=APP_PORT)
        # training_pipeline = TrainPipeline()
        # training_pipeline.run_pipeline()
    except Exception as e:
        print(e)