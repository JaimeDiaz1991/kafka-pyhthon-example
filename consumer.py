# consumer.py
from __future__ import print_function  # python 2/3 compatibility
 
import sys # used to exit
from kafka import KafkaConsumer
 
KAFKA_TOPIC = 'python-6'
KAFKA_BROKERS = ['localhost:9092','localhost1:9092','localhost3:9092']
GROUP_ID = 'change1'
 
consumer = KafkaConsumer(KAFKA_TOPIC, group_id=GROUP_ID, bootstrap_servers=KAFKA_BROKERS, 
                         auto_offset_reset='earliest')

try:
    for message in consumer:
        print(message.value)
except KeyboardInterrupt:
    sys.exit()