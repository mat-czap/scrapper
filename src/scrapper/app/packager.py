import pickle
from enum import Enum


class StatusPackage(Enum):
    PROCESSING = 0
    END = 1

# todo consider add dataclasses to package
class Packager:
    """ Packager is responsible for:

          1. Pass serialized info (in "package") to Worker
          2. Keep state of completion scrapped urls, in order to inform worker about last element
    """

    def __init__(self, payload):
        self.number_of_links = self._get_payload_length(payload)
        self._realization = 0

    def _get_payload_length(self, payload):
        return len(payload["urls"])

    def _increase(self):
        self._realization += 1

    def send(self, url: str, batch_id: int) -> bytes:
        self._increase()
        package = {"url": url, "batch_id": batch_id}
        if self._realization == self.number_of_links:
            package["status"] = StatusPackage.END
            return pickle.dumps(package)
        else:
            package["status"] = StatusPackage.PROCESSING
            return pickle.dumps(package)
