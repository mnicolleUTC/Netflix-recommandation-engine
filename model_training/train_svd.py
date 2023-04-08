import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split
from surprise.dump import dump, load
from surprise.accuracy import mae, rmse
import datetime


def model_training():
    print("Training started at :")
    print(datetime.datetime.now())
    # Load data
    df = pd.read_csv("filtering.csv")

    # Prepare data for the surprise library
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[["Cust_Id", "Movie_Id", "Rating"]], reader)

    # Split data into train and test set
    trainset, testset = train_test_split(data, test_size=0.1)

    # Create and train the SVD model with increased factors and epochs.
    model = SVD(n_factors= 150, n_epochs=20, random_state=42)
    model.fit(trainset)

    # Save the trained model
    dump("model.pkl", algo=model)

    # Evaluate the model performance on the test set
    predictions = model.test(testset)

    print("MAE: ", mae(predictions))
    print("RMSE: ", rmse(predictions))
    print("Training ended at :")
    print(datetime.datetime.now())

# Function to get top n recommendations for a user
def get_top_n_recommendations(user_id = 245, n=10):
    # Load the trained model and data
    df = pd.read_csv("filtering.csv")
    df = df.drop(columns=["Timestamp"])
    _, loaded_model = load("model.pkl")

    # Get the list of all movie ids
    all_movie_ids = set(df["Movie_Id"].unique())

    # Get the list of movies already rated by the user
    rated_movies = set(df[df["Cust_Id"] == user_id]["Movie_Id"].tolist())

    # Get the list of movies not yet rated by the user
    not_rated_movies = all_movie_ids - rated_movies

    # Predict ratings for all unrated movies
    predictions = [(movie_id, loaded_model.predict(user_id, movie_id).est) for movie_id in not_rated_movies]

    # Get the top n movies with the highest predicted ratings
    top_n_movies = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]

    return top_n_movies

if __name__=="__main__":
    #
    #model_training()
    #List of ID user's to obtain different predictions
    # 785314, 243963, 1744889,1881982, 3423, 1596531
    print(get_top_n_recommendations(user_id=785314))

    