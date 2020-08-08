from scrapper.infrastructure import rabbit_connection_factory
from scrapper.infrastructure.scrapper_repository import ScrapperRepository
from scrapper.infrastructure.config import get_config
from scrapper.worker.queue_consumer import QueueConsumer
from scrapper.worker.worker import Worker
from scrapper.worker.scrapping_strategy import strategy_1

config = get_config()
connection = rabbit_connection_factory(config["RABBITMQ_URL"])
repository = ScrapperRepository(config["SQLALCHEMY_DATABASE_URI"])
worker = Worker(repository, strategy_1)
consumer = QueueConsumer(connection, worker)
consumer.run()