import time
from kafka import KafkaConsumer, KafkaProducer
import json
import random


consumer = KafkaConsumer('topic.api', bootstrap_servers='10.12.32.218:9092', enable_auto_commit=False, group_id='api_grp')
producer1 = KafkaProducer(bootstrap_servers='10.12.32.218:9092',
                          value_serializer=lambda m: json.dumps(m).encode('ascii'))

for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # e.g., for unicode: `message.value.decode('utf-8')`
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))

    value_msg = json.loads(message.value.decode('utf-8')) # dict {"key": "get_posts_with_author_list"}
    try:
        key_msg = message.key.decode('utf-8') #key=b'unique string for determine message 9929'
    except:
        consumer.commit()
        continue

    if value_msg["key"] == "get_posts_with_author_list":
        consumer.commit()
        # Query to DB
        res = f'some result from content_msa using kafka. rnd_{random.randint(0, 100)}'
        print('res =', res, 'key_msg =', key_msg)
        producer1.send(topic='topic.content', value={'key': res},
                             key=message.key)

