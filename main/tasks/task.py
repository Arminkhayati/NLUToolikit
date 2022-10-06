from abc import ABC, abstractmethod



class Task(ABC):

    def __init__(self, config: dict):
        """1- Create an instance of sentence generator for your task
           2- set a class variable for all words of your task.
           3- set a class variable for labels of your task.
           4- set a class variable for config
        """
        pass
    @abstractmethod
    def load_data(self) -> tuple:
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

    # @abstractmethod
    # def generate(self, template):
    #     """Generate a sentence from a template"""
    #     pass














