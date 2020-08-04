import pickle
import requests
from functools import wraps
from scrapper.app.packager import StatusPackage


class DataMissing(Exception):
    pass

#
# def data_checker(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         try:
#             if self._data is not None:
#                 return func(*args, **kwargs)
#             else:
#                 raise DataMissing
#         except DataMissing:
#             print("_data in Worker instance is not declared.Use self.set_data_from_queue()")
#         return
#
#     return wrapper


class Worker:
    def __init__(self, repository):
        # @todo określić typ dla _data
        self._data = 0
        self._repository = repository

    def set_data_from_queue(self, body):
        self._data = pickle.loads(body)

    def get_params_to_scrap(self):
        try:
            if self._data != 0:
                return self._data["url"]
            else:
                raise DataMissing
        except DataMissing:
            print("_data in Worker instance is not declared.Use self.set_data_from_queue()")

    def _add_links(self, scrapped_links):
        for page in scrapped_links:
            self._repository.add_link(self._data["url"], page, self._data["batch_id"])
        return "ok"

    def _update_batch(self):
        if self._data["status"] == StatusPackage.END:
            self._repository.update_batch_finished(self._data["batch_id"])
        else:
            pass

    def _update_backend(self):
        try:
            result = requests.get('http://127.0.0.1:5001/batch', verify=False)
            print(result)
        except requests.ConnectionError as e:
            print(e)

    def commit(self, scrapped_links):
        self._add_links(scrapped_links)
        self._update_batch()
        self._update_backend()