from main.core.model.builder import Builder
from main.core.model.conv_seq2seq_util import conv_seq2seq_criterion_parser, conv_seq2seq_optimizer_parser
from main.core.model.conv_seq2seq.model import Encoder, Decoder, Seq2Seq


class ConvSeq2SeqBuilder(Builder):

    def build_from_cfg(self, config, device=None):
        # create model
        encoder = Encoder(input_dim=config["model_params"]["vocab_size"],
                          emb_dim=config["model_params"]['embedding_dim'],
                          hid_dim=config["model_params"]['hidden_dim'],
                          n_layers=config["model_params"]['encoder_layers'],
                          kernel_size=config["model_params"]['kernel_size'],
                          dropout=config["model_params"]['dropout'],
                          device=device,
                          max_length=config["model_params"]['max_seq_len'],
                          )

        decoder = Decoder(output_dim=config["model_params"]["vocab_size"],
                          emb_dim=config["model_params"]['embedding_dim'],
                          hid_dim=config["model_params"]['hidden_dim'],
                          n_layers=config["model_params"]['decoder_layers'],
                          kernel_size=config["model_params"]['kernel_size'],
                          dropout=config["model_params"]['dropout'],
                          tgt_pad_idx=0,
                          device=device,
                          max_length=config["model_params"]['max_seq_len'],
                          )

        convs2s = Seq2Seq(encoder, decoder, device=device, )
        criterion = conv_seq2seq_criterion_parser(config["model_params"]["loss"]).to(device)
        optimizer = conv_seq2seq_optimizer_parser(config["model_params"]["optimizer"], convs2s)

        return convs2s, criterion, optimizer