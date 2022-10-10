
import torch

def conv_seq2seq_criterion_parser(loss):
    if loss == "CrossEntropyLoss":
        criterion = torch.nn.CrossEntropyLoss(ignore_index=0)
    else:
        criterion = torch.nn.CrossEntropyLoss()
    return criterion

def conv_seq2seq_optimizer_parser(optimizer, model):
    if optimizer["type"] == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=optimizer["learning_rate"])
        return optimizer
    else:
        return None