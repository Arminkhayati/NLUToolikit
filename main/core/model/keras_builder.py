from main.core.model.builder import Builder
from main.core.model.keras_util import keras_layer_parser, optimizer_parser, metric_parser
from keras.models import Model as keras_model


class KerasBuilder(Builder):

    def build_from_cfg(self, config, device=None):
        model = None
        for i, k in enumerate(config["model"].keys()):
            layer_conf = config["model"][k]
            if i == 0:
                model = keras_layer_parser(layer_conf)
                inputs = model
            else:
                model = keras_layer_parser(layer_conf)(model)
        optimizer = optimizer_parser(config["model_params"]["optimizer"])
        loss = config["model_params"]["loss"]
        metrics = metric_parser(config["model_params"]["metrics"])
        model = keras_model(inputs, model)
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model.summary()
        return model
