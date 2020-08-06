import functools
import pickle
import requests
from dataclasses import dataclass, field
from typing import Optional, Set
from scrapper.app.packager import StatusPackage
from scrapper.infrastructure.scrapper_repository import EncodedError


class DataMissingError(Exception):
    pass


@dataclass
class EncodedRawData:
    url: str
    batch_id: int
    status: StatusPackage


@dataclass
class ScrappedData:
    status: str = ""
    data: Set[Optional[str]] = field(default_factory=set)


def data_checker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        print(self._data)
        try:
            if self._data is not None:
                return func(*args, **kwargs)
            else:
                raise DataMissingError
        except DataMissingError:
            print("_data in Worker instance is not declared.Use self.set_data_from_queue()")
        return
    return wrapper


# todo convert into stateless class, pass result through methods.
class Worker:
    """ Worker:

           1. Operating layer between QueueConsumer and scrapper_repository
           2. Deserializes data from queue
           3. Informs Flask backend about finished Batch
           4. Applies scrapping_strategy

     """

    def __init__(self, repository, scraping_strategy):
        self._data: Optional[EncodedRawData] = None
        self._repository = repository
        self._scraping_strategy = scraping_strategy

    def _set_data_from_queue(self, raw_data_from_queue: bytes):
        deserialized_data = pickle.loads(raw_data_from_queue)
        self._data = EncodedRawData(deserialized_data["url"], deserialized_data["batch_id"], deserialized_data["status"])
    # deserialize data return encoded raw data

    @data_checker
    def _get_params_to_scrap(self) -> str:
        try:
            if self._data is not None:
                return self._data.url
            else:
                raise DataMissingError
        except DataMissingError:
            print("_data in Worker instance is not declared.Use self.set_data_from_queue()")

    # todo change adding single link to adding entire batch within transaction. Inspect "bulk_save_objects"
    @data_checker
    def _add_links(self, scrapped_links: ScrappedData):
        for page in scrapped_links.data:
            try:
                self._repository.add_link(self._data.url, page, self._data.batch_id)
            except EncodedError as e:
                print(f"Occurred problem with saving single link to db, it has been omitted : {page}")
                continue
        return

    def _update_batch(self):
        if self._data.status == StatusPackage.END:
            self._repository.update_batch_status(self._data.batch_id)
        else:
            pass

    def _update_backend(self):
        try:
            # zczytywanie hosta i portu
            result = requests.get('http://scrapper_web_1:5000/batch')
            print(result)
        except requests.ConnectionError as e:
            print(e)

    def _commit(self, scrapped_links: ScrappedData):
        self._add_links(scrapped_links)
        self._update_batch()
        # todo repair updating Flask backend
        self._update_backend()

    def scrap_job(self, raw_data_from_queue: bytes):
        self._set_data_from_queue(raw_data_from_queue)
        try:
            scrapped_links: ScrappedData = self._scraping_strategy(self._get_params_to_scrap())
            if scrapped_links.status == "ok":
                self._commit(scrapped_links)
            else:
                print("Worker failed scrapping")
        except Exception as ex:
            print("scrap_job: ", ex)