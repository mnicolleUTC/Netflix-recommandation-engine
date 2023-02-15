import pandas as pd
import numpy as np
import time 
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from joblib import dump
import mlflow
from mlflow import log_metric, log_param, log_artifacts
import os 

# Set tracking URI to your Heroku application
mlflow.set_tracking_uri(os.environ["https://mlflow-server-netflix.herokuapp.com/"])

if __name__ == "__main__":

    ### NECESSARY SETUP
    experiment_name="Netflix recommendation model"
    mlflow.set_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

    print("training model...")

    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog()

    df = pd.read_csv('data.csv', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])

    ### NECESSARY SETUP
    client = mlflow.tracking.MlflowClient()
    run = client.create_run(experiment.experiment_id)
    with mlflow.start_run(run_id = run.info.run_id) as run:

        reader = Reader()
        data = Dataset.load_from_df(df[['Cust_Id', 'Movie_Id', 'Rating']][:], reader)
        svd = SVD()
        #cross_validate(svd, data, measures=['RMSE', 'MAE'])

        mlflow.log_metric(cross_validate(svd, data, measures=['RMSE', 'MAE']))

        mlflow.sklearn.log_model(
            sk_model=svd,
            artifact_path="s3://mlflow-leadjedha/mlflow/",
            registered_model_name="mlflow_netflix"
        )

        dump(svd, 'model.joblib') 

        print("...Training Done!")
        print(f"---Total training time: {time.time()-start_time} seconds")