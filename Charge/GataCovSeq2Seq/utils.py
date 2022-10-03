import os
import yaml
import torch
import random
import numpy as np





def load_templates(path="Charge.txt", sos_eos=True, split=0.2, test_set=False):

    with open(path, encoding='utf-8') as f:
        templates = f.readlines()
        if sos_eos:
            templates = [['<sos>'] + line.strip().split(" ") + ['<eos>'] for line in templates]
        else:
            templates = [line.strip().split(" ") for line in templates]

    random.shuffle(templates)
    num_val_samples = int(split * len(templates))
    if test_set:
        num_train_samples = len(templates) - 2 * num_val_samples
        train_templates = templates[:num_train_samples]
        val_templates = templates[num_train_samples : num_train_samples + num_val_samples]
        test_templates = templates[num_train_samples + num_val_samples :]
    else:
        num_train_samples = len(templates) - num_val_samples
        train_templates = templates[:num_train_samples]
        val_templates = templates[num_train_samples : num_train_samples + num_val_samples]
        test_templates = []
    print(f"{len(templates)} total templates")
    print(f"{len(train_templates)} training templates")
    print(f"{len(val_templates)} validation templates")
    print(f"{len(test_templates)} test templates")
    return train_templates, val_templates, test_templates


def load_conf(conf_path="conf.yaml"):
    with open(conf_path, 'r') as stream:
        return yaml.safe_load(stream)

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs

def save_model(model):
    torch.save(model.state_dict(), os.path.join("checkpoint", 'bestmodel.pt'))


def load_model():
    return torch.load(os.path.join("checkpoint", 'bestmodel.pt'))
