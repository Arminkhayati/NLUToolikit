from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn.functional as F
import random
import torch


class TorchDataLoader(DataLoader):
    def __init__(self, templates, generator, x_tokenizer,
                 y_tokenizer, batch_size,
                 steps_per_epoch, shuffle,
                 device, collate_fn, aug_percent=0.0):
        dataset = TorchDataset(templates, generator, x_tokenizer,
                 y_tokenizer, steps_per_epoch,
                 device, aug_percent)
        super().__init__(dataset=dataset, batch_size=batch_size, shuffle=shuffle, collate_fn=collate_fn)



class TorchDataset(Dataset):
    def __init__(self, templates, generator, x_tokenizer,
                 y_tokenizer, steps_per_epoch,
                 device, aug_percent=0.0):
        self.templates = templates
        self.generator = generator
        self.x_tokenizer = x_tokenizer
        self.y_tokenizer = y_tokenizer
        self.steps_per_epoch = steps_per_epoch
        self.aug_percent = aug_percent
        self.device = device
        self.train = True


    def __generate_sentence_for(self, template):
        sentence, slots = self.generator.generate_from(template)
        self.x_tokenizer.set_train(self.train)
        self.y_tokenizer.set_train(False)
        sentence = self.x_tokenizer.words_to_seq(sentence)
        slots = self.y_tokenizer.words_to_seq(slots)
        return sentence, slots

    def __ohe_encoding(self, sequences):
        return F.one_hot(sequences, num_classes=len(self.y_tokenizer.word_to_index))

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

    def __getitem__(self, idx):
        # self.test.append(idx)
        template = random.choice(self.templates)
        template = self.__augment(template)
        sentence, slots = self.__generate_sentence_for(template)
        sentence = torch.tensor(sentence).to(self.device)
        slots = torch.tensor(slots).to(self.device)
        # slots = self.__ohe_encoding(slots)
        return sentence, slots