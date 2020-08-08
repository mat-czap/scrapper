import time
from scrapper.worker.worker import Worker


class QueueConsumer:
    def __init__(self, connection, worker: Worker):
        self._channel = connection.channel()
        self._worker = worker

    def run(self):
        self._channel.exchange_declare(exchange='logs', exchange_type='topic')
        result = self._channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        self._channel.queue_bind(exchange='logs', queue=queue_name, routing_key="#")
        print(' [*] Waiting for messages')
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(queue=queue_name, on_message_callback=self._callback)
        self._channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        self._worker.scrap_job(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)