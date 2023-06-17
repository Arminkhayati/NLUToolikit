import sys
sys.path.append("..")
import argparse
from keras.models import load_model
from keras_nlp.layers import TokenAndPositionEmbedding
import pickle
import numpy as np




def keras_model_evaluation(args):
    model = load_model(args["model"], custom_objects={'TokenAndPositionEmbedding': TokenAndPositionEmbedding})
    with open(args["x_tokenizer"], "rb") as input_file:
        x_tokenizer = pickle.load(input_file)
    with open(args["y_tokenizer"], "rb") as input_file:
        y_tokenizer = pickle.load(input_file)

    while True:
        sentence = input("Type :  ")
        if sentence == "exit":
            print("Bye Bye .")
            break
        sentence = sentence.strip().split(" ")
        sentence = [w for w in sentence if w != '']
        input_seq = x_tokenizer.words_to_seq(sentence)
        prediction = model.predict([input_seq])
        slots = [np.argmax(x) for x in prediction[0][:]]
        slots = y_tokenizer.seq_to_words(slots)
        slots = [s if s != 'OOV' else 'O' for s in slots]
        binded = list(zip(sentence, slots))
        for sen, slo in binded:
            print(slo, sen)




parser = argparse.ArgumentParser(prog="dataset_evaluator", description='Evaluating model on input text (type "exit" to quit)')
parser.add_argument(
    '-m', '--model',
    type=str,
    default="./output/model/RNNEncoder/full_model.h5",
    help='Path of model.',
)
parser.add_argument(
    '-xt', '--x-tokenizer',
    type=str,
    default='./output/data_dump/RNNEncoder/x_tokenizer.pickle',
    help='Path of X_Tokenizer pickle file.',
)
parser.add_argument(
    '-yt', '--y-tokenizer',
    type=str,
    default='./output/data_dump/RNNEncoder/y_tokenizer.pickle',
    help='Path of Y_Tokenizer pickle file.',
)


args = parser.parse_args().__dict__
# print(args)
keras_model_evaluation(args)




