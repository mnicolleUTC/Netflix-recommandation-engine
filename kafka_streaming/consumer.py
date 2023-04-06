from confluent_kafka import Consumer
import json
import ccloud_lib
import time
import pandas as pd
import numpy as np
import boto3
import pickle
from credentials import AWS_KEY_ID
from credentials import AWS_KEY_SECRET


# Kafka config
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "netflix_recommandation" 
consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
consumer_conf['group.id'] = 'netflix_reco'
consumer_conf['auto.offset.reset'] = 'latest'
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])

# Get title-id mapping for all movies
df_title = pd.read_csv('movie_titles.csv', encoding = "ISO-8859-1", header = None, names = ['Movie_Id', 'Year', 'Name'], on_bad_lines='skip')
df_title.set_index('Movie_Id', inplace = True)

# load recommendation model
_, svd = load("model.pkl")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            record_key = msg.key()
            record_value_bytes = msg.value()
            # Convert value to int
            record_value = int.from_bytes(record_value_bytes, 'big')
            print(f"received value = {record_value}")
            model_input = json.loads(str(record_value)) # input to feed to model : a user ID
            # Display the 10 most recommended movies for user :
            user_pred = df_title.copy() 
            user_pred = user_pred.reset_index()
            # No use of ML model due to low performance
            user_pred['Estimate_Score'] = user_pred['Movie_Id'].apply(lambda x: svd.predict(model_input, x).est)
            # Adding column User ID which always contain the same value which is user ID
            user_pred["User_Id"] = int(record_value)
            # Reorganize columns order
            user_pred = user_pred[['User_Id','Movie_Id','Year','Name','Estimate_Score']]
            user_pred.to_csv('last.csv', index=False)
            aws_access_key_id = AWS_KEY_ID
            aws_secret_access_key = AWS_KEY_SECRET
            s3 = boto3.client('s3', aws_access_key_id=AWS_KEY_ID,aws_secret_access_key=AWS_KEY_SECRET)
            with open("last.csv", "rb") as f:
                # Upload the file to S3
                s3.upload_fileobj(f, "netflix-recommandation", "last_recommandation/last.csv")
            time.sleep(0.01)
            print("success")
            
except KeyboardInterrupt:
    pass
finally:
    consumer.close()

