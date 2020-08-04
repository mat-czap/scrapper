import pickle
from enum import Enum


class PackagerBase:
    pass


class StatusPackage(Enum):
    PROCESSING = 0
    END = 1


class Packager:
    """ Packager is responsible for:

          1. Pass serialized info (in "package") for worker
          2. Keep state of completion scrapped urls, in order to inform worker about last element
    """

    def __init__(self, payload):
        self.number_of_links = len(payload["urls"])
        self._realization = 0

    def _increase(self):
        self._realization += 1

    def send(self, url: str, batch_id: int):
        self._increase()
        package = {"url": url, "batch_id": batch_id}
        if self._realization == self.number_of_links:
            package["status"] = StatusPackage.END
            return pickle.dumps(package)
        else:
            package["status"] = StatusPackage.PROCESSING
            return pickle.dumps(package)