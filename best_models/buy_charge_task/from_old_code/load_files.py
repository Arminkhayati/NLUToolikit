import pickle
from tensorflow.keras.models import load_model
import os
from keras_nlp.layers import TokenAndPositionEmbedding

class LoadFiles:

    def __init__(self, dir_path="./1"):
        self.dir_path = dir_path

    def load_all(self):
        model_path = os.path.join(self.dir_path, "charge_nlu.h5")
        model = load_model(model_path, custom_objects={'TokenAndPositionEmbedding': TokenAndPositionEmbedding})

        x_tokenizer_path = os.path.join(self.dir_path, "x_tokenizer.pickle")
        y_tokenizer_path = os.path.join(self.dir_path, "y_tokenizer.pickle")
        with open(x_tokenizer_path, "rb") as input_file:
            x_tokenizer = pickle.load(input_file)
        with open(y_tokenizer_path, "rb") as input_file:
            y_tokenizer = pickle.load(input_file)
        return model, x_tokenizer, y_tokenizer