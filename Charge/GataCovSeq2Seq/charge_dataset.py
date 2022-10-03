from torch.utils.data import Dataset
import sentence_from_template as sft
from tensorflow.keras.utils import to_categorical
import torch.nn.functional as F
import random
import torch

class ChargeDataset(Dataset):

    def __init__(self, templates, x_tokenizer, y_tokenizer, len_, device,
                 aug_percent=0.0, max_seq_len=45):
        self.templates =  templates
        self.x_tokenizer = x_tokenizer
        self.y_tokenizer = y_tokenizer
        self.max_seq_len = max_seq_len
        self.aug_percent = aug_percent
        self.len_ = len_
        self.device = device
        self.train = True
        # self.test = []

    def __generate_sentence_for(self, template):
        sentence, slots = sft.generate_sentence_from(template)
        # print(sentence)
        # print(slots)
        self.x_tokenizer.set_train(self.train)
        self.y_tokenizer.set_train(False)
        sentence = self.x_tokenizer.words_to_seq(sentence)
        slots = self.y_tokenizer.words_to_seq(slots)
        return sentence, slots

    def __ohe_encoding(self, sequences):
        return F.one_hot(sequences, num_classes=len(self.y_tokenizer.word_to_index))

    def __len__(self):
        return self.len_

    def __augment(self, template):
        if random.random() < self.aug_percent:
            random.shuffle(template)
        return template


    def __getitem__(self, idx):
        # self.test.append(idx)
        template = random.choice(self.templates)
        # template = self.__augment(template)
        sentence, slots = self.__generate_sentence_for(template)
        sentence = torch.tensor(sentence).to(self.device)
        slots = torch.tensor(slots).to(self.device)
        # slots = self.__ohe_encoding(slots)
        return sentence, slots
