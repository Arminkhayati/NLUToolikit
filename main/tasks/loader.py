from main.tasks.buy_charge.buy_charge_task import BuyChargeTask
from main.tasks.hotel_reservation.hotel_reservation_task import HotelReservationTask
from main.tasks.account_balance import AccountBalanceTask
from main.tasks.sentence_generator import SentenceGenerator

def task_loader(config):
    if config["task"] == "BuyChargeTask":
        return BuyChargeTask(config)
    elif config["task"] == "HotelReservationTask":
        return HotelReservationTask(config)
    elif config["task"] == "AccountBalanceTask":
        return AccountBalanceTask(config)
    else:
        raise RuntimeError("{0} Task Not Exists ...".format(config["task"]))

def generator_loader(config):
    if config["task"] == "BuyChargeTask":
        from main.tasks.buy_charge.buy_chrage_task_util import get_word_or_slot_value
        return SentenceGenerator(get_word_or_slot_value)
    elif config["task"] == "HotelReservationTask":
        from main.tasks.hotel_reservation.hotel_reservation_task_util import get_word_or_slot_value
        return SentenceGenerator(get_word_or_slot_value)
    elif config["task"] == "AccountBalanceTask":
        from main.tasks.account_balance import get_word_or_slot_value
        return SentenceGenerator(get_word_or_slot_value)
    else:
        raise RuntimeError("{0} Task Not Exists ...".format(config["task"]))