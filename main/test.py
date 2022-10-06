from omegaconf import OmegaConf
from main.core.train_handler import TrainHandler

yaml_path = "../configs/ChargeConfig.yaml"
# yaml_path = "../configs/HotelConfig.yaml"
config = OmegaConf.load(yaml_path)
trainer = TrainHandler(config)
trainer.train()

# print((config["callbacks"]["ModelCheckpoint"]))













