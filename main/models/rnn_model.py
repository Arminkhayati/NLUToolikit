from main.models.parser import layer_parser, optimizer_parser, metric_parser
from keras.models import Model


class RNNModel:

    def build(self, config):
        model = None
        for i, k in enumerate(config["model"].keys()):
            layer_conf = config["model"][k]
            if i == 0:
                model = layer_parser(layer_conf)
                inputs = model
            else:
                model = layer_parser(layer_conf)(model)
        optimizer = optimizer_parser(config["model_params"]["optimizer"])
        loss = config["model_params"]["loss"]
        metrics = metric_parser(config["model_params"]["metrics"])
        model = Model(inputs, model)
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
        model.summary()
        return model


