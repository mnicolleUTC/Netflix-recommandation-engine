import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from joblib import dump

df = pd.read_csv('data.csv', header = None, names = ['Cust_Id', 'Rating'], usecols = [0,1])

reader = Reader()
data = Dataset.load_from_df(df[['Cust_Id', 'Movie_Id', 'Rating']][:], reader)
svd = SVD()
cross_validate(svd, data, measures=['RMSE', 'MAE'])

dump(svd, 'model.joblib') 