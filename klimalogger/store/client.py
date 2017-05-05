from abc import ABCMeta, abstractmethod


class StoreClient(metaclass=ABCMeta):
    @abstractmethod
    def store(self, data):
        pass