from kafka import KafkaConsumer
from kafka import TopicPartition
import os
import datetime

from prediction import prediction as prediction
import pandas as pd
import tensorflow as tf
import sys
import json

consumer = KafkaConsumer(
    'JSO7',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id=None,
    auto_offset_reset='earliest')

consumer.subscribe('JSONFIN')
print("Consuming messages from Topic")
message = consumer.poll()

rowx=0
colx=0

#consumer.close(autocommit=True);

columns=['Zeit', 'Graz-DB', 'Graz-MG', 'Graz-S', 'Graz-OP', 'Graz-N', 'Graz-W', 'Lustb', 'Luftdruck']
#Empty Dataframe mit Index

dfAll = pd.DataFrame(columns=columns)

prediction_count = 0
message_count = 0
for message in consumer:

    df = pd.DataFrame([message.value])
    dfAll=dfAll.append(df)
    message_count += 1

    if message_count == 48:
        print(dfAll)
        print('blabla')
        prediction(dfAll)
       # tf.keras.backend.clear_session()
        print('successssssss', prediction_count)
        prediction_count +=1
        del dfAll
        dfAll = pd.DataFrame(columns=columns)
        message_count = 0
        if prediction_count == 1600:
            break


#print(dfAll)

#dfModel = dfAll



# Call prediction

#prediction(dfModel)
