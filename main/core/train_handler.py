from main.tasks.loader import task_loader
from main.core.train.keras_model_trainer import KerasModelTrainer

class TrainHandler:
    def __init__(self, config):
        self.config = config
        self.task = task_loader(config)


    def train(self):
        if self.config["name"] == "ConvSeq2Seq":
            pass
        else:
            return KerasModelTrainer(self.config, self.task).train()