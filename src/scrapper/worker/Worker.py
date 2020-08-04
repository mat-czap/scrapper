import pickle
from dataclasses import dataclass

import requests
from functools import wraps
from scrapper.app.packager import StatusPackage


class DataMissing(Exception):
    pass

# Decorator for class method checking if _data is already populated
#
# def data_checker(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             if self._data != 0:
#                 return func(*args, **kwargs)
#             else:
#                 raise DataMissing
#         except DataMissing:
#             print("_data in Worker instance is not declared.Use self.set_data_from_queue()")
#         return
#
#     return wrapper


@dataclass
class ScrappedData:
    status: str
    data: set


class Worker:
    def __init__(self, repository):
    # def __init__(self, repository,scrap_strategy):
        self._data = 0
        self._repository = repository

    def set_data_from_queue(self, body: bytes):
        self._data = pickle.loads(body)

    def get_params_to_scrap(self):
        try:
            if self._data != 0:
                return self._data["url"]
            else:
                raise DataMissing
        except DataMissing:
            print("_data in Worker instance is not declared.Use self.set_data_from_queue()")

    def _add_links(self, scrapped_links: ScrappedData) -> None:
        for page in scrapped_links.data:
            try:
                self._repository.add_link(self._data["url"], page, self._data["batch_id"])
            except Exception as e:
                print(f"Occurred problem with saving single link to db, it has been omitted : {page}")
                continue
        return

    def _update_batch(self):
        if self._data["status"] == StatusPackage.END:
            self._repository.update_batch_status(self._data["batch_id"])
        else:
            pass

    def _update_backend(self) -> None:
        try:
            result = requests.get('http://localhost:5001/batch')
        except requests.ConnectionError as e:
            print(e)

    def commit(self, scrapped_links: ScrappedData):
        self._add_links(scrapped_links)
        self._update_batch()
        # todo repair updating Flask backend
        # self._update_backend()

    # def scrap_job(self,body: bytes):
    #
    #     self._set_data_from_queue(body)
    #     scrapping_input = self._get_params_to_scrap()
    #
    #     try:
    #         scrapped_links: ScrappedData = self._scrap_strategy(scrapping_input)
    #         if scrapped_links.status == "ok":
    #             worker.commit(scrapped_links)
    #         else:
    #             print("Worker failed scrapping")
    #
    #     except Exception as ex:
    #         print("scrap_job: ", ex)
