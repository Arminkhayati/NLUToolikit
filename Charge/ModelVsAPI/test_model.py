import numpy as np
from load_files import LoadFiles

class TestModel:

    def __init__(self, dir_path="./1"):
        self.dir_path = dir_path
        loader = LoadFiles(self.dir_path)
        self.model, self.x_tokenizer, self.y_tokenizer = loader.load_all()

    def test_sentence(self, sentence):
        sentence =sentence.strip().split(" ")
        sentence = [w for w in sentence if w != '']
        input_seq = self.x_tokenizer.words_to_seq(sentence)
        prediction = self.model.predict([input_seq])
        slots = [np.argmax(x) for x in prediction[0][:]]
        slots = self.y_tokenizer.seq_to_words(slots)
        slots = [s if s != 'O' else 'هیچ' for s in slots  ]
        binded = list(zip(sentence, slots))
        print(binded)
        for sen, slo in binded:
            if slo != "هیچ" :
                print(slo, sen)
        return binded