import sentence_from_template as sft
from tensorflow.keras.utils import Sequence
from tensorflow.keras.utils import to_categorical
import numpy as np
import random

class DataGenerator(Sequence):
    def __init__(self, templates, x_tokenizer, y_tokenizer, batch_size, len_,
                 aug_percent=0.1, max_seq_len=45):
        self.templates =  templates
        self.batch_size = batch_size
        self.x_tokenizer = x_tokenizer
        self.y_tokenizer = y_tokenizer
        self.max_seq_len = max_seq_len
        self.len_ = len_
        self.aug_percent = aug_percent
        self.train = True

    def __generate_sentence_for(self, template):
        sentence, slots = sft.generate_sentence_from(template)
        self.x_tokenizer.set_train(self.train)
        self.y_tokenizer.set_train(self.train)
        sentence = self.x_tokenizer.words_to_seq(sentence)
        slots = self.y_tokenizer.words_to_seq(slots)
        return sentence, slots

    def __ohe_encoding(self, sequences):
        return to_categorical(sequences, num_classes=len(self.y_tokenizer.word_to_index))

    def __len__(self):
        return self.len_

    def __augment(self, template):
        if random.random() < self.aug_percent:
            random.shuffle(template)
        return template

    def __getitem__(self, index):
        templates = random.choices(self.templates, k=self.batch_size)
        X, y = [], []
        for t in templates:
            t = self.__augment(t)
            sentence, slots = self.__generate_sentence_for(t)
            X.append(sentence)
            y.append(slots)
        X = np.array(X)
        # X = X[:,:, np.newaxis]
        # X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        y = np.array(y)
        y = self.__ohe_encoding(y)
        return X, y