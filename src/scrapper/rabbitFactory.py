import pika


def rabbit_context(config):
    parameters = pika.URLParameters(config['RABBITMQ_URL'])
    connection = pika.BlockingConnection(parameters)
    return connection
