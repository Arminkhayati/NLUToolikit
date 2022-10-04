import yaml
from tasks.buy_charge.buy_charge_task import BuyChargeTask
from tasks.hotel_reservation.hotel_reservation_task import HotelReservationTask
from models.rnn_model import RNNModel
from omegaconf import OmegaConf




def task_loader(config):
    if config["task"] == "BuyChargeTask":
        return BuyChargeTask()
    elif config["task"] == "HotelReservationTask":
        return HotelReservationTask()
    else:
        raise RuntimeError("{0} Task Not Exists ...".format(config["task"]))


yaml_path = "../configs/ChargeConfig.yaml"
config = OmegaConf.load(yaml_path)
model = RNNModel().build(config)
