import pickle
import requests


class Worker:
    def __init__(self, data, repository):
        self._data = self._get_deserielized_data(data)
        self._repository = repository

    def _get_deserielized_data(self, raw_data):
        return pickle.loads(raw_data)

    # todo return only 2 first params
    def get_params_to_scrap(self):
        return self._data
    # todo logic from tasks.py about adding to db links
    def _add_links(self, scrapped_links):
        pass

    def _update_batch(self):
        if len(self._data) == 2:
            pass
        else:
            self._repository.update_batch_finished(self._data["batch_id"])

    def _update_backend(self):
        status = requests.get('http://localhost:5001/batch')
        print(status)

    def commit(self, scrapped_links):
        self._add_links(scrapped_links)
        self._update_batch()
        self._update_backend()
