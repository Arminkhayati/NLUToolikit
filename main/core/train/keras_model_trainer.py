from main.core.model.keras_builder import KerasBuilder
from main.util.tokenizer import Tokenizer
from main.core.dataset.keras_data_generator import KerasDataGenerator
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import pickle
import os
from pathlib import Path

class KerasModelTrainer:
    def __init__(self, config, task):
        self.config = config
        self.task = task
        if not os.path.exists(config["data"]["save_data_dir"]):
            os.makedirs(config["data"]["save_data_dir"])
        if not os.path.exists(config["save_model_dir"]):
            os.makedirs(config["save_model_dir"])


    def train(self):
        self.templates, self.train_templates, self.val_templates, self.test_templates = self.task.load_data()
        self.x_tokenizer = self.__create_tokenizer("x")
        self.y_tokenizer = self.__create_tokenizer("y")
        self.model = KerasBuilder().build_from_cfg(self.config)
        train_data_gen = KerasDataGenerator(self.train_templates, self.task.generator,
                                            self.x_tokenizer, self.y_tokenizer,
                                            self.config["model_params"]["batch_size"],
                                            self.config["model_params"]["steps_per_epoch"],
                                            aug_percent=self.config["data"]["augmentation"])

        val_data_gen = KerasDataGenerator(self.val_templates, self.task.generator,
                                          self.x_tokenizer, self.y_tokenizer,
                                          self.config["model_params"]["batch_size"],
                                          self.config["model_params"]["validation_steps"],
                                          aug_percent=self.config["data"]["augmentation"])
        head, _ = os.path.split(self.config["callbacks"]["ModelCheckpoint"]["filepath"])
        Path(head).mkdir(parents=True, exist_ok=True)
        checkpoint = ModelCheckpoint(**self.config["callbacks"]["ModelCheckpoint"])
        reduceLROnPlat = ReduceLROnPlateau(**self.config["callbacks"]["ReduceLROnPlateau"])
        tsboard = TensorBoard(**self.config["callbacks"]["TensorBoard"])
        callbacks_list = [checkpoint, reduceLROnPlat, tsboard]
        history = self.model.fit(train_data_gen,
                            epochs=self.config["model_params"]["epochs"],
                            steps_per_epoch=self.config["model_params"]["steps_per_epoch"],
                            validation_steps=self.config["model_params"]["validation_steps"],
                            validation_data=val_data_gen,
                            callbacks=callbacks_list, )
        self.__save_data()
        return history

    def __create_tokenizer(self, type):
        if type == "x":
            return Tokenizer(num_words=self.config["model_params"]["num_words"],
                             max_seq_len=self.config["model_params"]["max_seq_len"],
                             words=self.task.words,
                             sos_eos=self.config["data"]["add_sos_eos"])
        elif type == "y":
            return Tokenizer(num_words=self.config["model_params"]["num_words"],
                             max_seq_len=self.config["model_params"]["max_seq_len"],
                             labels=self.task.labels,
                             sos_eos=self.config["data"]["add_sos_eos"])
        return None

    def __save_data(self):
        self.model.load_weights(self.config["callbacks"]["ModelCheckpoint"]["filepath"])
        path = self.config["save_model_dir"]
        Path(path).mkdir(parents=True, exist_ok=True)
        path = os.path.join(path, "full_model.h5")
        self.model.save(path)

        Path(self.config["data"]["save_data_dir"]).mkdir(parents=True, exist_ok=True)
        path = os.path.join(self.config["data"]["save_data_dir"], "x_tokenizer.pickle")
        with open(path, "wb") as f:
            self.x_tokenizer.set_train(False)
            pickle.dump(self.x_tokenizer, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "y_tokenizer.pickle")
        with open(path, "wb") as f:
            self.y_tokenizer.set_train(False)
            pickle.dump(self.y_tokenizer, f)

        path = os.path.join(self.config["data"]["save_data_dir"], "all_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "train_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.train_templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "validation_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.val_templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "test_data.pickle")
        with open(path, "wb") as f:
                pickle.dump(self.test_templates, f)
        # path = os.path.join(self.config["data"]["save_data_dir"], "task.pickle")
        # with open(path, "wb") as f:
        #     pickle.dump(self.task, f)