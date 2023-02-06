import requests
import json
import pandas as pd
import numpy as np


def get_data_from_api():
    """
    Get data from Jedha API to generate 10 movies/users
    Output of API is not fromatted as JSON. An additionnal step will be 
    necessary (see function convert_to_dataframe)

    Returns:
        dict_value: Dictionnary containing values generated from the API.
    """
    url = "https://jedha-netflix-real-time-api.herokuapp.com/"\
          "users-currently-watching-movie"
    response = requests.request("GET", url)
    str_dict_value = response.json()
    dict_value = json.loads(str_dict_value)
    return dict_value

def convert_to_dataframe(data):
    """
    Convert the dictionnary containing values generated from the API into a 
    clean dataframe
    
    Args:
        data (dict): Dictionnary containing values generated from the API 

    Returns:
        df (pd.DataFrame): Dataframe containing formatted values.
    """
    data_arr = np.array(data["data"])
    year_release = data_arr[:,0]
    movie_name = data_arr[:,1]
    current_time = data_arr[:,2]
    customer_ID = data_arr[:,3]
    data_formatted = {
        "YearRelease":year_release,
        "Name":movie_name,
        "current_time":current_time,
        "customerID":customer_ID,
    }
    df = pd.DataFrame(data = data_formatted)
    return df

def obtain_movie():
    """
    Main function of the program that get information from API and formatted it 
    into a DataFrame with dict format

    Returns:
        df_dict (pd.DataFrame): Dataframe in dict format containing formatted values.
    """
    data = get_data_from_api()
    df = convert_to_dataframe(data)
    df_dict = df.to_dict()
    return df_dict

if __name__ =="__main__":
    df = obtain_movie()
    