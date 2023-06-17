import random
import logging
logging.basicConfig(level=logging.INFO)
import pickle
import os


def load_templates_from_text_file(config):
    with open(config["data"]["data_path"], encoding='utf-8') as f:
        templates = f.readlines()
        templates = [line.strip().split(" ") for line in templates]
    random.seed(config["seed"])
    random.shuffle(templates)
    num_val_samples = int(config["data"]["split"] * len(templates))
    if config["data"]["use_test_set"]:
        num_train_samples = len(templates) - 2 * num_val_samples
        train_templates = templates[:num_train_samples]
        val_templates = templates[num_train_samples: num_train_samples + num_val_samples]
        test_templates = templates[num_train_samples + num_val_samples:]
    else:
        num_train_samples = len(templates) - num_val_samples
        train_templates = templates[:num_train_samples]
        val_templates = templates[num_train_samples: num_train_samples + num_val_samples]
        test_templates = []

    print("*********************")
    print(train_templates)
    print("*********************")
    print(val_templates)
    print("*********************")
    logging.log(logging.INFO, f" {len(templates)} templates loaded")
    logging.log(logging.INFO, f" {len(train_templates)} templates selected for training")
    logging.log(logging.INFO, f" {len(val_templates)} templates selected for validation")
    logging.log(logging.INFO, f" {len(test_templates)} templates selected for test")
    return templates, train_templates, val_templates, test_templates


def load_templates_from_pickle_file(config):
    with open(config["data"]["train_data"], "rb") as f:
        train_templates = pickle.load(f)
    with open(config["data"]["validation_data"], "rb") as f:
        val_templates = pickle.load(f)
    if config["data"]["use_test_set"]:
        with open(config["data"]["test_data"], "rb") as f:
            test_templates = pickle.load(f)
    else:
        test_templates = []
    templates = train_templates + val_templates + test_templates
    logging.log(logging.INFO, f" {len(templates)} templates loaded")
    logging.log(logging.INFO, f" {len(train_templates)} templates selected for training")
    logging.log(logging.INFO, f" {len(val_templates)} templates selected for validation")
    logging.log(logging.INFO, f" {len(test_templates)} templates selected for test")
    return templates, train_templates, val_templates, test_templates


