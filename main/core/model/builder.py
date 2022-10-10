from abc import ABC, abstractmethod



class Builder(ABC):

    @abstractmethod
    def build_from_cfg(self, config: dict, device: str):
        """This method takes config dictionary and device (in case of using torch model)
            and builds model.
        """
        pass