import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from joblib import dump
import time 

df = pd.read_csv('data.csv', index_col=0)

print("training model...")

reader = Reader()
data = Dataset.load_from_df(df[['Cust_Id', 'Movie_Id', 'Rating']][:], reader)
svd = SVD()
cross_validate(svd, data, measures=['RMSE', 'MAE'])

dump(svd, 'model_fully_train.joblib')

print("...Training Done!")
print(f"---Total training time: {time.time()-start_time} seconds")