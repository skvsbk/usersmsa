import time
import json
from uuid import uuid4
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException



topic_prod = "topic.content"
topic_cons = "topic.api"

producer = Producer({'bootstrap.servers': '10.12.32.218:9092'})

conf = {'bootstrap.servers': '10.12.32.218:9092',
        'group.id': "content_grp",
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'}

consumer = Consumer(conf)
consumer.subscribe([topic_cons])

try:
    while True:
        print("Listening")
        # read single message at a time
        msg = consumer.poll(0)

        if msg is None:
            time.sleep(1)
            continue
        if msg.error():
            print("Error reading message : {}".format(msg.error()))
            continue
        # You can parse message and save to data base here
        print(msg)
        consumer.commit() # (asynchronous=False)
        producer.produce(topic_prod, key='key_12345'.encode(),
                         value=json.dumps({'key': 'sfcvdfvdegbvrfgb'}).encode('ascii'))

except Exception as ex:
    print("Kafka Exception : {}", ex)

finally:
    print("closing consumer")
    consumer.close()