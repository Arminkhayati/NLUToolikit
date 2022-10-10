from main.tasks.hotel_reservation.hotel_reservation_task_util import get_word_or_slot_value, ALL_WORDS
from main.tasks.sentence_generator import SentenceGenerator
from main.tasks.util import load_templates_from_pickle_file
from main.tasks.util import load_templates_from_text_file
from main.tasks.task import Task
import os

class HotelReservationTask(Task):
    def __init__(self, config: dict):
        # Create a SentenceGenerator instance with your task util get_word_or_slot_value function
        # Don't forget to import your task util get_word_or_slot_value function above.
        self.generator = SentenceGenerator(get_word_or_slot_value)
        self.words = ALL_WORDS
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

    def _handle_text(self) -> tuple:
        """Add path of text file in config file"""
        self.config["data"]["data_path"] = \
            os.path.join(self.config["data"]["data_dir"], "Hotel.txt")
        return load_templates_from_text_file(self.config)

    def _handle_pickle(self) -> tuple:
        """Add paths of train, validation and test pickle files in config file"""
        self.config["data"]["train_data"] = \
            os.path.join(self.config["data"]["data_dir"], "train_hotel.pickle")
        self.config["data"]["validation_data"] = \
            os.path.join(self.config["data"]["data_dir"], "validation_hotel.pickle")
        self.config["data"]["test_data"] = \
            os.path.join(self.config["data"]["data_dir"], "test_hotel.pickle")
        return load_templates_from_pickle_file(self.config)

    # def generate(self, template):
    #     """Generate a sentence from a template"""
    #     return self.generator.generate_from(template)















