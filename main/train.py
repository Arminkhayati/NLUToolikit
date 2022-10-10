from omegaconf import OmegaConf
import sys
sys.path.append("..")
from main.core.train_handler import TrainHandler
import argparse

def pars_args():
    parser = argparse.ArgumentParser(prog="Train Model", description='Train model from Config.yaml file.')
    parser.add_argument(
        '-c', '--config',
        type=str,
        default='/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/configs/ChargeConfig.yaml',
        help='Path of Config.yaml file.',
    )

    args = parser.parse_args().__dict__
    return args

if __name__ == "__main__" and __package__ is None:
    # yaml_path = "/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/configs/CovSeq2Seq.yaml"
    # yaml_path = "../configs/HotelConfig.yaml"
    args = pars_args()
    config = OmegaConf.load(args["config"])
    trainer = TrainHandler(config)
    trainer.train()















