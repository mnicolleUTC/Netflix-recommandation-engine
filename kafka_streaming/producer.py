from confluent_kafka import Producer
import json
import ccloud_lib # Library not installed with pip but imported from ccloud_lib.py
import numpy as np
import time
import datetime
from API_results import obtain_movie # Personnal function defined in a local file


# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "netflix_recommandation"

# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer = Producer(producer_conf)

# Create topic if it doesn't already exist
ccloud_lib.create_topic(CONF, TOPIC)


delivered_records = 0

# Callback called acked (triggered by poll() or flush())
# when a message has been successfully delivered or
# permanently failed delivery (after retries).
def acked(err, msg):
    global delivered_records
    # Delivery report handler called on successful or failed delivery of message
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
                .format(msg.topic(), msg.partition(), msg.offset()))

try:
    while True:
        data = obtain_movie()
        time_extract = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        id_user = data["customerID"][0]
        print("Producing record - time: {0}\tUserID: {1}"\
            .format(time_extract, id_user))
        # Convert integer id_user to bytes
        id_user_bytes = int(id_user).to_bytes((int(id_user).bit_length() + 7) // 8, 'big')
        # This will actually send data to your topic
        producer.produce(
            TOPIC,
            key="netflix",
            value=id_user_bytes,
            on_delivery=acked
        )
        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls thanks to acked callback
        producer.poll(0)
        time.sleep(12)
except KeyboardInterrupt:
    pass
finally:
    producer.flush() # Finish producing the latest event before stopping the whole script
