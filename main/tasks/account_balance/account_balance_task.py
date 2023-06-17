from main.tasks.sentence_generator import SentenceGenerator
from main.tasks.account_balance.account_balance_task_util import get_word_or_slot_value, get_all_words
from main.tasks.util import load_templates_from_pickle_file
from main.tasks.util import load_templates_from_text_file
from main.tasks.task import Task
import os


class AccountBalanceTask(Task):
    def __init__(self, config: dict):
        """1- Create an instance of sentence generator for your task
           2- set a class variable for all words of your task.
           3- set a class variable for labels of your task.
           4- set a class variable for config
        """
        # Create a SentenceGenerator instance with your task util get_word_or_slot_value function
        # Don't forget to import your task util get_word_or_slot_value function above.

        self.generator = SentenceGenerator(get_word_or_slot_value)
        self.words = get_all_words()
        self.labels = config["data"]["labels"]
        self.config = config


    def load_data(self) -> tuple:
        """Loading data from text or pickle files"""

        if self.config["data"]["from"] == "text":
            return self._handle_text()
        elif self.config["data"]["from"] == "pickle":
            return self._handle_pickle()
        else:
            raise RuntimeError("{0} Is Not A Valid Data File ...".format(self.config["from"]))


    def _handle_pickle(self) -> tuple:
        """Add paths of train, validation and test pickle files in config file"""

        self.config["data"]["train_data"] = \
            os.path.join(self.config["data"]["data_dir"], "train_data.pickle")
        self.config["data"]["validation_data"] = \
            os.path.join(self.config["data"]["data_dir"], "validation_data.pickle")
        self.config["data"]["test_data"] = \
            os.path.join(self.config["data"]["data_dir"], "test_data.pickle")
        return load_templates_from_pickle_file(self.config)


    def _handle_text(self) -> tuple:
        """Add paths of text file in config file"""

        self.config["data"]["data_path"] = \
            os.path.join(self.config["data"]["data_dir"], "Account_Balance.txt")
        return load_templates_from_text_file(self.config)


    # def generate(self, template):
    #     """Generate a sentence from a template"""
    #     pass