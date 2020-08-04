from scrapper.infrastructure import rabbit_connection_factory
from scrapper.infrastructure.scrapper_repository import ScrapperRepository
from scrapper.worker.Worker import Worker, ScrappedData
from scrapper.worker.config import get_config
from scrapper.worker.scrap_strategy import scrap_by_url

config = get_config()
connection = rabbit_connection_factory(config.get("RABBITMQ_URL"))
repository = ScrapperRepository(config["SQLALCHEMY_DATABASE_URI"])

channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='logs', queue=queue_name, routing_key="#")
print(' [*] Waiting for messages. To exit press CTRL+C')


# worker = Worker(repository,scrap_strategy)
worker = Worker(repository)


# class RabbitConsumer:
#     def __init__(self, connection, worker: Worker):
#         self._connection = connection
#         self._worker = worker
#         self._channel = self._connection.channel()
#
#     def _run(self):
#         channel.exchange_declare(exchange='logs', exchange_type='topic')
#         result = channel.queue_declare(queue='', exclusive=True)
#         queue_name = result.method.queue
#         channel.queue_bind(exchange='logs', queue=queue_name, routing_key="#")
#         print(' [*] Waiting for messages. To exit press CTRL+C')
#         channel.basic_qos(prefetch_count=1)
#         channel.basic_consume(queue=queue_name, on_message_callback=self._callback)
#         channel.start_consuming()
#
#     def _callback(self,ch, method, properties, body):
#         self._worker.scrap_job(body)
#         ch.basic_ack(delivery_tag=method.delivery_tag)


def scrap_job(worker: Worker, body: bytes):

    worker.set_data_from_queue(body)
    scrapping_input = worker.get_params_to_scrap()

    try:
        scrapped_links: ScrappedData = scrap_by_url(scrapping_input)
        if scrapped_links.status == "ok":
            worker.commit(scrapped_links)
        else:
            print("Worker failed scrapping")

    except Exception as ex:
        print("scrap_job: ", ex)


def callback(ch, method, properties, body):
    scrap_job(worker, body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()

