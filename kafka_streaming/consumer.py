from confluent_kafka import Consumer
import json
import ccloud_lib
import time
import pandas as pd
import os

CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "netflix_recommandation" 
consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
consumer_conf['group.id'] = 'my_tesla_stock_watcher'
consumer_conf['auto.offset.reset'] = 'latest'
consumer = Consumer(consumer_conf)
consumer.subscribe([TOPIC])

# Load global df in csv format in order to store values
namefile = "local_data_storage.csv"
if namefile in os.listdir('.'):
    df = pd.read_csv(namefile, sep=";", names = ["datetime","current_price"])
else :
    df = pd.DataFrame(columns = ["datetime","current_price"])
    df.to_csv(namefile,header = False, index = False)
try:
    while True:
        # With direct transmission 
        """
        msg = consumer.poll(1.0)
        if msg is None:
            print("Waiting for message or event/error in poll()")
            continue
        elif msg.error():
            print('error: {}'.format(msg.error()))
        else:
            record_key = msg.key()
            record_value = msg.value()
            data = json.loads(record_value)
            print(data)
            print(f"At {data['time_of_price']}, the Tesla stock price is {data['current_price']}$")
            time.sleep(1)
        """
        # With waiting 10 messages before saving
        print("Collecting 5 new messages")
        msg = consumer.consume(num_messages=5,timeout=10)
        print("Messages collected")
        if msg is None:
            # No message available within timeout.
            # Initial message consumption may take up to
            # `session.timeout.ms` for the consumer group to
            # rebalance and start consuming
            print("Waiting for message or event/error in poll()")
            continue
        else:
            # Useless to print message because non readable 
            # print("### Un-processed msg")
            # print(msg)
            print("### Value msg")
            h_msg = [json.loads(x.value()) for x in msg]
            df_temp = pd.DataFrame.from_dict(h_msg)
            print(df_temp)
            print("Adding those row to global dataframe")
            df = pd.concat([df,df_temp], axis=0)
            
except KeyboardInterrupt:
    # Saving all data before exiting
    df.to_csv(namefile,header = False, index = False)
    print("Success for saving data")
    pass
finally:
    consumer.close()

