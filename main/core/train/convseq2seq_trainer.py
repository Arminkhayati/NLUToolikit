from main.core.model.conv_seq2seq_builder import ConvSeq2SeqBuilder
from main.util.tokenizer import Tokenizer
from main.core.dataset.torch_dataloader import TorchDataLoader
from torch.nn.utils.rnn import pad_sequence
from tensorboardX import SummaryWriter
from datetime import datetime
import pickle
import torch
import time
import math
import os


def collate_fn(batch):
    PAD_IDX = 0
    src_batch, tgt_batch = [], []
    for src_sample, tgt_sample in batch:
        src_batch.append(src_sample)
        tgt_batch.append(tgt_sample)
    src_batch = pad_sequence(src_batch, padding_value=PAD_IDX, batch_first=True)
    tgt_batch = pad_sequence(tgt_batch, padding_value=PAD_IDX, batch_first=True)
    return src_batch, tgt_batch


class ConvSeq2SeqTrainer:
    def __init__(self, config, task):
        self.config = config
        self.task = task
        if not os.path.exists(config["data"]["save_data_dir"]):
            os.makedirs(config["data"]["save_data_dir"])
        if not os.path.exists(self.config["save_model_dir"]):
            os.makedirs(self.config["save_model_dir"])

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def train(self):
        self.templates, self.train_templates, self.val_templates, self.test_templates = self.task.load_data()
        self.x_tokenizer = self.__create_tokenizer("x")
        self.y_tokenizer = self.__create_tokenizer("y")
        train_dataloader = TorchDataLoader(self.train_templates, self.task.generator,
                                           self.x_tokenizer, self.y_tokenizer,
                                           self.config["model_params"]["batch_size"],
                                           self.config["model_params"]["steps_per_epoch"],
                                           True, self.device, collate_fn,
                                           aug_percent=self.config["data"]["augmentation"]
                                           )
        valid_dataloader = TorchDataLoader(self.val_templates, self.task.generator,
                                           self.x_tokenizer, self.y_tokenizer,
                                           self.config["model_params"]["batch_size"],
                                           self.config["model_params"]["steps_per_epoch"],
                                           True, self.device, collate_fn,
                                           aug_percent=self.config["data"]["augmentation"]
                                           )
        self.model, criterion, optimizer = ConvSeq2SeqBuilder().build_from_cfg(self.config, self.device)

        log_dir = self.config["callbacks"]["TensorBoard"]["log_dir"]
        log_dir = os.path.join(log_dir, datetime.now().strftime('%Y%m%d%H%M'))
        tb_writer = SummaryWriter(log_dir)

        best_valid_loss = float('inf')
        clip = self.config["model_params"]["clip"]
        for epoch in range(self.config["model_params"]["epochs"]):
            start_time = time.time()
            train_loss = self.__train_epoch(self.model, train_dataloader, optimizer, criterion, clip)
            valid_loss = self.__evaluate(self.model, valid_dataloader, criterion)
            end_time = time.time()

            epoch_mins, epoch_secs = self.__epoch_time(start_time, end_time)

            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                path = os.path.join(self.config["save_model_dir"], 'best_model_dict.pt')
                torch.save(self.model.state_dict(), path)

            tb_writer.add_scalar("Train_Loss", train_loss, epoch)
            # tb_writer.add_scalar("Train_PPL", math.exp(train_loss), epoch)
            tb_writer.add_scalar("Val_Loss", valid_loss, epoch)
            # tb_writer.add_scalar("Val_PPL", math.exp(valid_loss), epoch)
            print(f'Epoch: {epoch + 1:02} | Time: {epoch_mins}m {epoch_secs}s')
            print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
            print(f'\t Val. Loss: {valid_loss:.3f} |  Val. PPL: {math.exp(valid_loss):7.3f}')

        self.__save_data()
        return

    def __train_epoch(self, model, data_loader, optimizer, criterion, clip):
        model.train()
        epoch_loss = 0
        for src, tgt in data_loader:
            optimizer.zero_grad()
            output, _ = model(src, tgt[:, :-1])
            output_dim = output.shape[-1]
            output = output.contiguous().view(-1, output_dim)
            tgt = tgt[:, 1:].contiguous().view(-1)
            loss = criterion(output, tgt)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
            optimizer.step()
            epoch_loss += loss.item()
        return epoch_loss / len(data_loader)

    def __evaluate(self, model, data_loader, criterion):
        model.eval()
        epoch_loss = 0
        with torch.no_grad():
            for src, tgt in data_loader:
                output, _ = model(src, tgt[:, :-1])
                output_dim = output.shape[-1]
                output = output.contiguous().view(-1, output_dim)
                tgt = tgt[:, 1:].contiguous().view(-1)
                loss = criterion(output, tgt)
                epoch_loss += loss.item()
        return epoch_loss / len(data_loader)

    def __create_tokenizer(self, type):
        if type == "x":
            return Tokenizer(num_words=self.config["model_params"]["num_words"],
                             max_seq_len=self.config["model_params"]["max_seq_len"],
                             words=self.task.words,
                             sos_eos=self.config["data"]["add_sos_eos"])
        elif type == "y":
            return Tokenizer(num_words=self.config["model_params"]["num_words"],
                             max_seq_len=self.config["model_params"]["max_seq_len"],
                             labels=self.task.labels,
                             sos_eos=self.config["data"]["add_sos_eos"])
        return None

    def __epoch_time(self, start_time, end_time):
        elapsed_time = end_time - start_time
        elapsed_mins = int(elapsed_time / 60)
        elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
        return elapsed_mins, elapsed_secs

    def __save_data(self):
        path = os.path.join(self.config["save_model_dir"], 'best_model_dict.pt')
        state_dict = torch.load(path)
        self.model.load_state_dict(state_dict)
        path = os.path.join(self.config["save_model_dir"], 'best_full_model.pt')
        torch.save(self.model, path)


        path = os.path.join(self.config["data"]["save_data_dir"], "x_tokenizer.pickle")
        with open(path, "wb") as f:
            self.x_tokenizer.set_train(False)
            pickle.dump(self.x_tokenizer, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "y_tokenizer.pickle")
        with open(path, "wb") as f:
            self.y_tokenizer.set_train(False)
            pickle.dump(self.y_tokenizer, f)

        path = os.path.join(self.config["data"]["save_data_dir"], "all_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "train_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.train_templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "validation_data.pickle")
        with open(path, "wb") as f:
            pickle.dump(self.val_templates, f)
        path = os.path.join(self.config["data"]["save_data_dir"], "test_data.pickle")
        with open(path, "wb") as f:
                pickle.dump(self.test_templates, f)
        # path = os.path.join(self.config["data"]["save_data_dir"], "task.pickle")
        # with open(path, "wb") as f:
        #     pickle.dump(self.task, f)