import abc
import pandas as pd


class LoaderBase():
    def __init__(self):
        pass

    @abc.abstractmethod
    def raw_cases(self) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def raw_deaths(self) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def cases(self) -> pd.DataFrame:
        pass

    @abc.abstractmethod
    def deaths(self) -> pd.DataFrame:
        pass
