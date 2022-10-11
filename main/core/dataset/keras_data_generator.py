from keras.utils import Sequence
from keras.utils import to_categorical
import numpy as np
import random

class KerasDataGenerator(Sequence):
    def __init__(self, templates, generator, x_tokenizer,
                 y_tokenizer, batch_size,
                 steps_per_epoch, aug_percent=0.0):

        self.templates =  templates
        self.generator = generator
        self.batch_size = batch_size
        self.x_tokenizer = x_tokenizer
        self.y_tokenizer = y_tokenizer
        self.steps_per_epoch = steps_per_epoch
        self.aug_percent = aug_percent
        self.train = True

    def __generate_sentence_for(self, template):
        sentence, slots = self.generator.generate_from(template)
        self.x_tokenizer.set_train(self.train)
        self.y_tokenizer.set_train(False)
        sentence = self.x_tokenizer.words_to_seq(sentence)
        slots = self.y_tokenizer.words_to_seq(slots)
        return sentence, slots

    def __ohe_encoding(self, sequences):
        return to_categorical(sequences, num_classes=len(self.y_tokenizer.word_to_index))

    def __len__(self):
        return self.steps_per_epoch

    def __augment(self, template):
        template = " ".join(template)
        template = template.split("#_#")
        if random.random() < self.aug_percent:
            random.shuffle(template)
        template = [w.strip() for w in template]
        template = " ".join(template)
        template = template.split(" ")
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
        y = np.array(y)
        y = self.__ohe_encoding(y)
        return X, y