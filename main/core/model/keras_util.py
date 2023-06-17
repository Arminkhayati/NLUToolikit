from keras import regularizers
from keras.models import Sequential, Model
from keras.layers import BatchNormalization, LayerNormalization, Embedding, LSTM, GRU, Dense, Bidirectional, TimeDistributed, Input, Dropout
from keras.metrics import Precision, Recall, Accuracy
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping, TensorBoard, LambdaCallback
import pandas as pd
import numpy as np
import re
import itertools
import random
from keras_nlp.layers import PositionEmbedding, TokenAndPositionEmbedding
from keras_nlp.layers import TransformerEncoder
import pickle



def keras_layer_parser(config):
    layer = config["layer"]
    if layer == "input":
        return input_parser(config)
    elif layer == "TokenAndPositionEmbedding":
        return token_and_positional_embedding_parser(config)
    elif layer == "Embedding":
        return embedding_parser(config)
    elif layer == "dropout":
        return dropout_parser(config)
    elif layer == "rnn":
        if ("bidirectional" in config.keys()) and config["bidirectional"]:
            return bidirectional_rnn(config)
        else:
            return rnn_parser(config)
    elif layer == "dense":
        if ("time_distributed" in config.keys()) and config["time_distributed"]:
            return time_distributed_dense_parser(config)
        else:
            return dense_parser(config)
    elif layer == "TransformerEncoder":
        return transformer_encoder_parser(config)
    elif layer == "LayerNormalization":
        return layer_normalization_parser(config)
    else:
        raise RuntimeError("{0} layer is not available ...".format(layer))


def input_parser(config):
    return Input(shape=config["shape"])

def token_and_positional_embedding_parser(config):
    return TokenAndPositionEmbedding(
        vocabulary_size=config["vocabulary_size"],
        sequence_length=config["sequence_length"],
        embedding_dim=config["embedding_dim"]
    )
def embedding_parser(config):
    return Embedding(
        input_dim=config["vocabulary_size"],
        input_length=config["sequence_length"],
        output_dim=config["embedding_dim"]
    )

def dropout_parser(config):
    return Dropout(config["rate"])

def regulizer_parser(config):
    if config["type"] == "L1":
        regularizers.L1(config["value"])
    elif config["type"] == "L2":
        regularizers.L2(config["value"])
    elif config["type"] == "L1L2":
        regularizers.L1L2(config["value"])

def rnn_parser(config):

    if config["type"] == "GRU":
        return GRU(config["num_units"], activation=config["activation"],
           return_sequences=config["return_sequences"],
           use_bias=config["use_bias"],
           kernel_regularizer=regulizer_parser(config["kernel_regularizer"]),
           recurrent_regularizer=regulizer_parser(config["recurrent_regularizer"]),
           bias_regularizer=regulizer_parser(config["bias_regularizer"]),
           activity_regularizer=regulizer_parser(config["activity_regularizer"]),
           dropout=config["dropout"],
           recurrent_dropout=config["recurrent_dropout"],
           )
    elif config["type"] == "LSTM":
        return LSTM(config["num_units"], activation=config["activation"],
           return_sequences=config["return_sequences"],
           use_bias=config["use_bias"],
           kernel_regularizer=regulizer_parser(config["kernel_regularizer"]),
           recurrent_regularizer=regulizer_parser(config["recurrent_regularizer"]),
           bias_regularizer=regulizer_parser(config["bias_regularizer"]),
           activity_regularizer=regulizer_parser(config["activity_regularizer"]),
           dropout=config["dropout"],
           recurrent_dropout=config["recurrent_dropout"],
            )
def bidirectional_rnn(config):
    return Bidirectional(rnn_parser(config))

def dense_parser(config):
    return Dense(config["dim"], activation=config["activation"])

def time_distributed_dense_parser(config):
    return TimeDistributed(dense_parser(config))

def optimizer_parser(config):
    optimizer = config["type"]
    lr = config["learning_rate"]
    if optimizer == "adam":
        return Adam(learning_rate=lr)
    else:
        return None

def transformer_encoder_parser(config):
    return TransformerEncoder(
        config["intermediate_dim"],
        config["num_heads"],
        dropout=config["dropout"],
        activation=config["activation"],
        layer_norm_epsilon=config["layer_norm_epsilon"]
    )

def layer_normalization_parser(config):
    return LayerNormalization()


def metric_parser(metrics):
    metrics_object = []
    for metric in metrics:
        if metric == "precision":
            metrics_object.append(Precision())
        elif metric == "recall":
            metrics_object.append(Recall())
        elif metric == "accuracy":
            metrics_object.append(Accuracy())
    return metrics_object


