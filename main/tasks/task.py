from abc import ABC, abstractmethod


class Task(ABC):

    @abstractmethod
    def load_data(self, config: dict) -> tuple:
        """Loading data from text or pickle files"""
        pass

    @abstractmethod
    def _handle_pickle(self) -> tuple:
        """Add paths of train, validation and test pickle files in config file"""
        pass

    @abstractmethod
    def _handle_text(self) -> tuple:
        """Add paths of text file in config file"""
        pass
















