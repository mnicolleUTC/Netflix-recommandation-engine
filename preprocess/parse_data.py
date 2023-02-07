import pandas as pd
import numpy as np


def parse_df(file):
    global_df = pd.DataFrame()
    with open (file,"r") as file :
        text = file.read()
        text_split = text.split(":")
        last_elt = len(text_split) - 1
    for i, elt in enumerate(text_split):
        # First element =  only a number
        if i == 0:
            index_film = int(elt)
            continue
        elif i == last_elt:
            continue
        else : 
            df_temp = create_dataframe_from_movie(elt,index_film)
            index_film +=1
            global_df = pd.concat([global_df,df_temp])
    return(global_df)   
                
        
def create_dataframe_from_movie(extract,index_movie):
    # List columns
    columns_df = ["Cust_Id","Rating","Timestamp"]
    # Eliminating last number 
    extract = "\n".join(extract.split('\n')[:-1])
    with open ("temp.csv","w") as file:
        file.write(extract)
    df = pd.read_csv("temp.csv",lineterminator='\n',sep = ",",header = None)
    df.columns = columns_df
    df["Movie_Id"] = int(index_movie)
    df.drop("Timestamp",axis = 1,inplace = True)
    print(df.head())
    return df

if __name__ =="__main__":
    df_all = pd.DataFrame()
    list_file = [
        "combined_data_1.txt",
        "combined_data_2.txt",
        "combined_data_3.txt",
        "combined_data_4.txt",
    ]
    for file in list_file:
        df_part = parse_df(file)
        df_all = pd.concat([df_all,df_part])
        df_all.to_csv("data.csv")
        
