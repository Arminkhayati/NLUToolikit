import sys
sys.path.append("..")
import argparse
import pickle
import numpy as np
import torch
from translation import find_slots_from

def conv_s2s_model_evaluation(args):
    with open(args["x_tokenizer"], "rb") as input_file:
        x_tokenizer = pickle.load(input_file)
    with open(args["y_tokenizer"], "rb") as input_file:
        y_tokenizer = pickle.load(input_file)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.load(args["model"])
    while True:
        sentence = input("Type :  ")
        if sentence == "exit":
            print("Bye Bye .")
            break
        translation, _ = find_slots_from(sentence, model, x_tokenizer, y_tokenizer, device, max_len=args["max_seq_len"])
        print(f'predicted trg = {translation}')






parser = argparse.ArgumentParser(prog="dataset_evaluator", description='Evaluating model on input text (type "exit" to quit)')
parser.add_argument(
    '-m', '--model',
    type=str,
    default="/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/model/ConvSeq2Seq/best_full_model.pt",
    help='Path of model.',
)
parser.add_argument(
    '-xt', '--x-tokenizer',
    type=str,
    default='/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/data_dump/ConvSeq2Seq/x_tokenizer.pickle',
    help='Path of X_Tokenizer pickle file.',
)
parser.add_argument(
    '-yt', '--y-tokenizer',
    type=str,
    default='/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/data_dump/ConvSeq2Seq/y_tokenizer.pickle',
    help='Path of Y_Tokenizer pickle file.',
)

parser.add_argument(
    '-msl', '--max-seq-len',
    type=int,
    default=45,
    help='Maximum sequence length for trained model. Default is 45.',
)


args = parser.parse_args().__dict__
# print(args)
conv_s2s_model_evaluation(args)
