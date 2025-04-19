import abc
from datetime import datetime


class AbstractPredictor(abc.ABC):

    @abc.abstractmethod
    def forecast(self, timestamp: str):
        raise NotImplementedError

    @abc.abstractmethod
    def refit(self, data):
        raise NotImplementedError

    @abc.abstractmethod
    def retrain(self, data):
        raise NotImplementedError

