import pickle
import requests
from dataclasses import dataclass, field
from typing import Optional, Set
from scrapper.app.packager import StatusPackage
from scrapper.infrastructure.scrapper_repository import EncodedError


class DataMissingError(Exception):
    pass


@dataclass
class EncodedData:
    url: str
    batch_id: int
    status: StatusPackage


@dataclass
class ScrappedData:
    data: EncodedData
    scrapped_status: str = False
    links: Set[Optional[str]] = field(default_factory=set)


class Worker:
    """ Worker:

           1. Operating layer between QueueConsumer and scrapper_repository
           2. Deserializes data from queue
           3. Informs Flask backend about finished Batch
           4. Applies scrapping_strategy

     """

    def __init__(self, repository, scraping_strategy):
        self._repository = repository
        self._scraping_strategy = scraping_strategy

    def _deserialize_data(self, raw_data: bytes):
        deserialized_data = pickle.loads(raw_data)
        encoded_row_data = EncodedData(deserialized_data["url"], deserialized_data["batch_id"],
                                       deserialized_data["status"])
        return encoded_row_data

    def _add_links(self, scrapped_links: ScrappedData):
        for page in scrapped_links.links:
            try:
                self._repository.add_link(scrapped_links.data.url, page, scrapped_links.data.batch_id)
            except EncodedError as e:
                print(f"Occurred problem with saving single link to db, it has been omitted : {page}")
                continue
        return

    def _update_batch(self, status_package, batch_id):
        if status_package == StatusPackage.END:
            self._repository.update_batch_status(batch_id)
        else:
            pass

    def _update_backend(self, batch_id):
        try:
            requests.post('http://scrapper_web_1:5000/batch', json={"batch_id": batch_id})

        except requests.ConnectionError as e:
            print(e)

    def _commit(self, scrapped_links: ScrappedData):
        self._add_links(scrapped_links)
        self._update_batch(scrapped_links.data.status, scrapped_links.data.batch_id)
        self._update_backend(scrapped_links.data.batch_id)

    def scrap_job(self, raw_data_from_queue: bytes):
        encoded_data: EncodedData = self._deserialize_data(raw_data_from_queue)
        try:
            scrapped_links = self._scraping_strategy(encoded_data)
            if scrapped_links.scrapped_status is True:
                self._commit(scrapped_links)
            else:
                print("Worker failed scrapping")
        except Exception as ex:
            print("scrap_job: ", ex)



# def data_checker(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         self = args[0]
#         print(self._data)
#         try:
#             if self._data is not None:
#                 return func(*args, **kwargs)
#             else:
#                 raise DataMissingError
#         except DataMissingError:
#             print("_data in Worker instance is not declared.Use self.set_data_from_queue()")
#         return
#     return wrapper

