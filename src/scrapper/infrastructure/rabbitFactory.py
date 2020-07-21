from typing import Dict
import pika

def rabbit_connection_factory(rabbitMQ_URL: str):
    parameters = pika.URLParameters(rabbitMQ_URL)
    connection = pika.BlockingConnection(parameters)
    return connection
