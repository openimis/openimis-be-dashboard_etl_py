from abc import ABC, abstractclassmethod


class ETLBase(ABC):

    # @abstractclassmethod
    # def run_etl(self): pass

    @abstractclassmethod
    def extract(self): pass

    @abstractclassmethod
    def transform(self, data): pass

    @abstractclassmethod
    def load(self, data): pass
