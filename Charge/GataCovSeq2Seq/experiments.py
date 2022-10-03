from charge_dataset import ChargeDataset
import random
from tokenizer import Tokenizer
import torch
from torch.utils.data import DataLoader
from utils import  *
from model import *
from train import train

TEST_SET = False
CONF = load_conf()
CONF["special_tokens"] = {
    # CONF["unk_token"]: 1,
    CONF["pad_token"]: 0,
    # CONF["sos_token"]: 12,
    # CONF["eos_token"]: 13,
}


# set seed
set_seed(CONF['seed'])

# get device
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# DEVICE = torch.device('cpu')


# load templates
train_templates, val_templates, test_templates = load_templates(path="Charge.txt", sos_eos=True,
                                                                split=0.2, test_set=TEST_SET)
# Create Tokenizers
x_tokenizer = Tokenizer(num_words=CONF["num_words"], max_seq_len=CONF["max_length"],
                        for_sentence=True)
y_tokenizer = Tokenizer(num_words=CONF["num_words"], max_seq_len=CONF["max_length"],
                        for_sentence=False, sos_eos=True)

# Create Datasets
train_dataset = ChargeDataset(train_templates, x_tokenizer, y_tokenizer, CONF["num_train_data"], DEVICE)
valid_dataset = ChargeDataset(val_templates, x_tokenizer, y_tokenizer, CONF["num_val_data"], DEVICE)
if TEST_SET:
    test_dataset = ChargeDataset(test_templates, x_tokenizer, y_tokenizer, CONF["num_val_data"], DEVICE)

# get data loaders
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
valid_dataloader = DataLoader(valid_dataset, batch_size=32, shuffle=True)
if TEST_SET:
    test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=True)

# create model
encoder = Encoder(input_dim = CONF["num_words"]*2,
                  emb_dim = CONF['embed_size'],
                  hid_dim = CONF['hidden_size'],
                  n_layers = CONF['encoder_layers'],
                  kernel_size = CONF['kernel_size'],
                  dropout = CONF['dropout'],
                  device = DEVICE,
                  max_length=CONF['max_length'],
                  )

decoder = Decoder(output_dim = CONF["num_words"]*2,
                  emb_dim = CONF['embed_size'],
                  hid_dim = CONF['hidden_size'],
                  n_layers = CONF['decoder_layers'],
                  kernel_size = CONF['kernel_size'],
                  dropout = CONF['dropout'],
                  tgt_pad_idx = CONF["special_tokens"][CONF['pad_token']],
                  device = DEVICE,
                  max_length=CONF['max_length'],
                  )

convs2s = Seq2Seq(encoder, decoder, device = DEVICE,)
# create optimizer and criterion
optimizer = torch.optim.Adam(convs2s.parameters())
criterion = torch.nn.CrossEntropyLoss(ignore_index = CONF["special_tokens"][CONF['pad_token']]).to(DEVICE)

# train
train(  convs2s,
        criterion,
        train_dataloader,
        valid_dataloader,
        optimizer,
        CONF["epochs"],
        CONF["clip"],
        )


