from main.tasks.loader import task_loader



class TrainHandler:
    def __init__(self, config):
        self.config = config
        self.task = task_loader(config)


    def train(self):
        if self.config["name"] == "ConvSeq2Seq":
            from main.core.train.convseq2seq_trainer import ConvSeq2SeqTrainer
            return ConvSeq2SeqTrainer(self.config, self.task).train()
        else:
            from main.core.train.keras_model_trainer import KerasModelTrainer
            return KerasModelTrainer(self.config, self.task).train()