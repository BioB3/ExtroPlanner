import abc


class AbstractPredictor(abc.ABC):
    @abc.abstractmethod
    def forecast(self, timestamp: str):
        raise NotImplementedError

    @abc.abstractmethod
    def refit(self, data):
        raise NotImplementedError
