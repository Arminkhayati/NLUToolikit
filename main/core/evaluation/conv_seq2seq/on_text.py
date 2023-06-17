import sys
sys.path.append("..")
import argparse
import pickle
import numpy as np
from translation import find_slots_from
import torch

def conv_s2s_model_evaluation(args):
    with open(args["x_tokenizer"], "rb") as input_file:
        x_tokenizer = pickle.load(input_file)
    with open(args["y_tokenizer"], "rb") as input_file:
        y_tokenizer = pickle.load(input_file)
    with open(args["text"], encoding="utf-8") as input_file:
        lines = input_file.readlines()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.load(args["model"])

    for i, sentence in enumerate(lines):
        print(f"Sentence {i+1}: {sentence}")
        translation, _ = find_slots_from(sentence, model, x_tokenizer, y_tokenizer, device, max_len=args["max_seq_len"])
        print(f'predicted trg = {translation}')


parser = argparse.ArgumentParser(prog="dataset_evaluator", description='Evaluating model on input text (type "exit" to quit)')
parser.add_argument(
    '-txt', '--text',
    type=str,
    default="./data/test.txt",
    help='Path of text file containing your sentences.',
)
parser.add_argument(
    '-m', '--model',
    type=str,
    default="./output/model/ConvSeq2Seq/best_full_model.pt",
    help='Path of model.',
)
parser.add_argument(
    '-xt', '--x-tokenizer',
    type=str,
    default='./output/data_dump/ConvSeq2Seq/x_tokenizer.pickle',
    help='Path of X_Tokenizer pickle file.',
)
parser.add_argument(
    '-yt', '--y-tokenizer',
    type=str,
    default='./output/data_dump/ConvSeq2Seq/y_tokenizer.pickle',
    help='Path of Y_Tokenizer pickle file.',
)

parser.add_argument(
    '-msl', '--max-seq-len',
    type=int,
    default=45,
    help='Maximum sequence length for trained model. Default is 45.',
)


args = parser.parse_args().__dict__
conv_s2s_model_evaluation(args)
