from opensearchpy import OpenSearch
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka import KafkaError, KafkaException
from loguru import logger
from schema_registry import schema_registry_client_config
import sys
from confluent_brokers import cluster_config

def create_opensearch_client():
    # Connection string to the OpenSearch Docker container
    conn_string = "http://localhost:9200"

    # Create the OpenSearch client without security
    client = OpenSearch(
        hosts=[conn_string],
    )

    return client

def create_opensearch_index(client: OpenSearch, index_name: str):
    # Create the index on OpenSearch if not exists
    if not client.indices.exists(index_name):
        client.indices.create(index_name)
        logger.info(f"Index {index_name} created")
    else:
        logger.info(f"Index {index_name} already exists")

def create_topic_avro_deserializer(schema_registry_client_config: dict):
    schema_registry_client = SchemaRegistryClient(schema_registry_client_config)
    avro_deserializer = AvroDeserializer(schema_registry_client=schema_registry_client)
    return avro_deserializer

running = True
def msg_process(msg, index_name, opensearch_client: OpenSearch):
    """Send JSON data to OpenSearch"""
    if msg is None:
        logger.warning("Incompatible message received")
        return

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                (msg.topic(), msg.partition(), msg.offset()))
        elif msg.error():
            raise KafkaException(msg.error())
    else:
        value = msg.value()
        logger.info(f"Putting user {value} to index {index_name}")
        # Send the value data to OpenSearch
        record = opensearch_client.index(
            index=index_name,
            body=value
        )
        logger.info(f"Sent to OpenSearch, {record}")

def basic_consume_loop(
        kafka_consumer: DeserializingConsumer, 
        topics:str,
        kafka_topic:str,
        opensearch_client: OpenSearch
        ):
    try:
        opensearch_consumer.subscribe(topics)
        logger. info(f"Subscribed to {topics}")
        while running:
            msg = kafka_consumer.poll(timeout=1.0) #offset commit occured here if auto.commit and auto.commit.interval.ms has pased.
            msg_process(
                msg=msg.value(), 
                index_name=kafka_topic,
                opensearch_client=opensearch_client
                )
                
    finally:
        # Close down consumer to commit final offsets.
        kafka_consumer.close()


def shutdown():
    running = False

if __name__ == "__main__":
    kafka_topic = "topic-user-avro"

    # OpenSearch client
    opensearch_client = create_opensearch_client()
    create_opensearch_index(opensearch_client, kafka_topic)

    # Kafka consumer client
    avro_deserializer = create_topic_avro_deserializer(schema_registry_client_config)
    cluster_config.update({
        'group.id': 'opensearch-consumer-group-3',
        'value.deserializer': avro_deserializer,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'false'
    })
    opensearch_consumer = DeserializingConsumer(cluster_config)
    topics = [kafka_topic]

    # Start consuming messages
    basic_consume_loop(opensearch_consumer, topics, kafka_topic, opensearch_client)
    # shutdown()