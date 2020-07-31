import pickle


class PackagerBase:
    pass


class Packager:
    def __init__(self, payload):
        self.nr_links = len(payload)
        self._realization = 0

    def _increase(self):
        self._realization += 1

    def send(self, url, batch_id):
        self._increase()
        package = [url, batch_id]
        if self._realization == self.nr_links:
            return pickle.dumps(package.append("end"))
        else:
            return pickle.dumps(package)