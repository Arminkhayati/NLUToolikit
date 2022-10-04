from main.tasks.util import load_templates_from_pickle_file
from main.tasks.util import load_templates_from_text_file
from main.tasks.task import Task
import os

class BuyChargeTask(Task):

    def load_data(self, config: dict) -> tuple:
        """Loading data from text or pickle files"""
        self.config = config
        if config["data"]["from"] == "text":
            return self._handle_text()
        elif config["data"]["from"] == "pickle":
            return self._handle_pickle()
        else:
            raise RuntimeError("{0} Is Not A Valid Data File ...".format(config["from"]))

    def _handle_text(self) -> tuple:
        """Add paths of train, validation and test pickle files in config file"""
        self.config["data"]["data_path"] = \
            os.path.join(self.config["data"]["data_dir"], "Charge.txt")
        return load_templates_from_text_file(self.config)

    def _handle_pickle(self) -> tuple:
        """Add paths of text file in config file"""
        self.config["data"]["train_data"] = \
            os.path.join(self.config["data"]["data_dir"], "train_charge.pickle")
        self.config["data"]["validation_data"] = \
            os.path.join(self.config["data"]["data_dir"], "validation_charge.pickle")
        self.config["data"]["test_data"] = \
            os.path.join(self.config["data"]["data_dir"], "test_charge.pickle")
        return load_templates_from_pickle_file(self.config)

















