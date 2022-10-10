import argparse
from keras.models import load_model
from keras_nlp.layers import TokenAndPositionEmbedding
import pickle
import numpy as np

def keras_model_predictor(args):
    model = load_model(args["model"], custom_objects={'TokenAndPositionEmbedding': TokenAndPositionEmbedding})
    with open(args["x_tokenizer"], "rb") as input_file:
        x_tokenizer = pickle.load(input_file)
    with open(args["y_tokenizer"], "rb") as input_file:
        y_tokenizer = pickle.load(input_file)

    def tokenize_sentence(sentence):
        sentence = sentence.strip().split(" ")
        sentence = [w for w in sentence if w != '']
        input_seq = x_tokenizer.words_to_seq(sentence)
        prediction = model.predict([input_seq])
        slots = [np.argmax(x) for x in prediction[0][:]]
        slots = y_tokenizer.seq_to_words(slots)
        return sentence, slots

    return tokenize_sentence


def get_predictor(args):
    return keras_model_predictor(args)







