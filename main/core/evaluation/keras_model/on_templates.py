import sys
sys.path.append("..")
import argparse
import pathlib
import pickle
from main.tasks.loader import generator_loader
from keras.models import load_model
from main.core.dataset.keras_data_generator import KerasDataGenerator
from keras_nlp.layers import TokenAndPositionEmbedding

def keras_model_evaluation(args):
    model = load_model(args["model"], custom_objects={'TokenAndPositionEmbedding': TokenAndPositionEmbedding})
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

    data_gen = KerasDataGenerator(templates, generator,
                                  x_tokenizer, y_tokenizer,
                                  args["batch_size"],
                                  args["steps_per_epoch"],
                                  aug_percent=args["augmentation"])
    data_gen.train = False
    model_score = model.evaluate(data_gen, batch_size=args["batch_size"])

    # print("Your model score is:")
    # print(model_score)


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
    default='./output/data_dump/RNNEncoder/validation_data.pickle',
    help='Path of templates pickle file.',
)

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
# print(args)
keras_model_evaluation(args)

