from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_brokers import producer_config, schema_registry_client_config
from loguru import logger
from user_v2 import User
from dataclasses import asdict
from typing import Callable

def create_producer(config: dict):
    """Create a new producer instance using the provided configuration"""
    producer = Producer(producer_config)
    return producer

def create_avro_serializer(
        schema_registry_client_config: dict,
        schema_str: str,
        config: dict = None
) -> Callable:
    """Create a new Avro serializer instance
    
    Args:
        schema_registry_client_config (dict): Configuration for the schema registry client
        schema_str (str): Avro schema string
        config (dict, optional): Additional configuration for the Avro serializer.
            If None, the default configuration will be used. 
    
    Returns:
        Callable: A function that can be used to serialize data using the Avro schema
    
    Notes:
        Avro Intesrting Features:
        - When the Producer switches to a new but compatiable schema (e.g. adding a new field), 
            the preupdate and postupdate consumers will still be able to read the data without errors.

        Caveats:
        - Arvo data requires a schema for both serialization and deserialization. 
        This means, the 2 write and read processes must be provided with the same schema. Unlike Arvo files -- the schema is included in the file itself, Kafka message needs special schema resolution.
        https://avro.apache.org/docs/1.7.7/spec.html#Schema+Resolution

        Schema Resolution implemented in ArvoSerializer: 
            - Producer sends message with Schema ID
            - Consumer uses Schema ID to fetch schema from Schema Registry
        
    
    """
    schema_registry_client = SchemaRegistryClient(schema_registry_client_config)
    _config = config or None
    avro_serializer = AvroSerializer(
        schema_registry_client,
        schema_str=schema_str,
        conf=_config
        )
    return avro_serializer


if __name__ == "__main__":
    # Preconfigured Confluent Kafka Topic
    kafka_topic = "topic-user-avro"

    # Create a producer instance
    # producer = Producer(producer_config)
    

    # Create data object
    schema_str = User.get_schema()
    value = asdict( User(1, "y consulting", "y@consulting.come"))

    # Create Avro Serializer
    avro_serializer = create_avro_serializer(
        schema_registry_client_config,
        schema_str
    )

    # Create Message Serialization Context
    serialization_context = SerializationContext(kafka_topic, MessageField.VALUE)
    # producer.produce(
    #     kafka_topic, 
    #     value=avro_serializer(value, serialization_context)
    # )
    producer_config['value.serializer'] = avro_serializer
    producer = SerializingProducer(producer_config)
    producer.produce(
        kafka_topic, value=value
    )
    producer.flush()
