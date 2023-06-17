import sys
sys.path.append("..")
import argparse
import pickle
import numpy as np

from main.core.model.conv_seq2seq_util import conv_seq2seq_criterion_parser
from translation import find_slots_from
import torch
from main.tasks.loader import generator_loader
import pathlib
from main.core.train.convseq2seq_trainer import collate_fn
from main.core.dataset.torch_dataloader import TorchDataLoader

def conv_s2s_model_evaluation(args):
    generator = generator_loader(args)

    extension = pathlib.Path(args["templates"]).suffix
    if extension == ".pickle":
        with open(args["templates"], "rb") as f:
            templates = pickle.load(f)
    elif extension == ".txt":
        with open(args["templates"], encoding='utf-8') as f:
            templates = f.readlines()
            templates = [line.strip().split(" ") for line in templates]
    else:
        raise RuntimeError("Templates file must be text or pickle, got : {0}".format(extension))

    with open(args["x_tokenizer"], "rb") as input_file:
        x_tokenizer = pickle.load(input_file)
    with open(args["y_tokenizer"], "rb") as input_file:
        y_tokenizer = pickle.load(input_file)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.load(args["model"])

    dataloader = TorchDataLoader(templates, generator,
                                 x_tokenizer, y_tokenizer,
                                 args["batch_size"],
                                 args["steps_per_epoch"],
                                 True, device, collate_fn,
                                 aug_percent=args["augmentation"])
    criterion = conv_seq2seq_criterion_parser("CrossEntropyLoss")

    model.eval()
    epoch_loss = 0
    with torch.no_grad():
        for src, tgt in dataloader:
            output, _ = model(src, tgt[:, :-1])
            output_dim = output.shape[-1]
            output = output.contiguous().view(-1, output_dim)
            tgt = tgt[:, 1:].contiguous().view(-1)
            loss = criterion(output, tgt)
            epoch_loss += loss.item()
    print("loss : ", epoch_loss / len(dataloader))


parser = argparse.ArgumentParser(prog="dataset_evaluator", description='Evaluating model on a given templates')

parser.add_argument(
    '-t', '--task',
    type=str,
    default='BuyChargeTask',
    help='Name of the task.',
)
parser.add_argument(
    '-tmp', '--templates',
    type=str,
    default='./output/data_dump/ConvSeq2Seq/validation_data.pickle',
    help='Path of templates pickle file.',
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
    '-b', '--batch-size',
    type=int,
    default=32,
    help='Batch size to load data.',
)

parser.add_argument(
    '-stpe', '--steps-per-epoch',
    type=int,
    default=3000,
    help='Number of steps in evaluation.',
)


parser.add_argument(
    '-aug', '--augmentation',
    type=int,
    default=3000,
    help='Augmentation ratio on data.',
)




args = parser.parse_args().__dict__
conv_s2s_model_evaluation(args)