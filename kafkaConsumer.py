from kafka import KafkaConsumer
from json import loads
consumer = KafkaConsumer(
    'results',
    bootstrap_servers=['kafka:9092', '0.0.0.0:9092', 'host.docker.internal:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8')))
print(consumer.bootstrap_connected())
for message in consumer:
    message = message.value
    print(message)
