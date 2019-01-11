# produ.py
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
import sys
#price dev_price_topic_output_local_test_test
#item dev_item_topic_output_local_test_test
KAFKA_TOPIC = 'dev_price_topic_output_local_test_test'
KAFKA_BROKERS = ['localhost:9092','localhost1:9092','localhost3:9092']
JSON_NAME = 'json/item.json'

def on_send_success(record_metadata):
    log.info(record_metadata.topic)
    log.info(record_metadata.partition)
    log.info(record_metadata.offset)


def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception

if len(sys.argv)>=2:
    KAFKA_TOPIC = sys.argv[1]
    print ('Setting KAFKA TOPIC to : '+ sys.argv[1])

if len(sys.argv)==3:
    JSON_NAME = sys.argv[2]
    print ('Setting JSON FILE to : ' + sys.argv[2])

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), bootstrap_servers=KAFKA_BROKERS)
# Asynchronous by default
with open(JSON_NAME) as f:
    data = json.load(f)
print(data)
future = producer.send(KAFKA_TOPIC, data).add_callback(on_send_success).add_errback(on_send_error)

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass


# block until all async messages are sent
producer.flush()

# configure multiple retries
#producer = KafkaProducer(retries=5)