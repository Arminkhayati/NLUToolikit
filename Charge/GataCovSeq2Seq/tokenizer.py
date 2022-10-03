import slot_util as su


PAD_VALUE = 0
OOV_VALUE = 1

WORD_TO_INDEX = {
    "PAD": PAD_VALUE,
    "O": OOV_VALUE,
    "charge_type":2,
    "bnumber":3,
    "pnumber":4,
    "amount":5,
    "operator":6,
    "unit":7,
    "charge_type_post":8,
    "bnumber_post":9,
    "pnumber_post":10,
    "operator_post":11,
}


class Tokenizer:
    def __init__(self, num_words=200, max_seq_len=45, for_sentence=True
                 , oov_token="<UNK>"
                 , pad_token="PAD"
                 , sos_eos=False):

        self.sos_eos = sos_eos
        self.for_sentence = for_sentence
        self.__check_for_sentence()
        self.oov_token = oov_token
        self.pad_token = pad_token
        self.num_words = num_words
        self.max_seq_len = max_seq_len
        self.train = True

    def __check_for_sentence(self):
        if self.for_sentence:
            # self.word_to_index = {"PAD":PAD_VALUE, oov_token:OOV_TOKEN}
            all_words = su.get_all_words()
            self.counter = {}
            self.word_to_index = {}
            for i, w in enumerate(all_words):
                # print(i+2)
                self.word_to_index[w] = i + 2 # Because of pad_value=0 and oov_value = 1
                self.counter[w] = 100000000
            self.index_to_word = {item[1] : item[0] for item in self.word_to_index.items()}
        else:
            self.__check_sos_eos()

    def __check_sos_eos(self):
        if self.sos_eos:
           self.word_to_index = WORD_TO_INDEX
           self.word_to_index["<sos>"]= 12
           self.word_to_index["<eos>"]= 13
           # print(" yes", self.word_to_index.keys())
           self.counter = {item[0]:0 for item in self.word_to_index.items()}
           self.index_to_word = {item[1] : item[0] for item in self.word_to_index.items()}
        else:
            self.word_to_index = WORD_TO_INDEX
            self.word_to_index.pop("<sos>", 'No Key found')
            self.word_to_index.pop("<eos>", 'No Key found')
            # print(" no", self.word_to_index.keys())
            self.counter = {item[0]:0 for item in self.word_to_index.items()}
            self.index_to_word = {item[1] : item[0] for item in self.word_to_index.items()}

    def __pad_sequences(self, sequence):
        while len(sequence) < self.max_seq_len:
            sequence.append(PAD_VALUE)
        return sequence

    def set_train(self, value):
        self.train = value

    def __insert_to_words(self, w):
        if len(self.word_to_index) > self.num_words:
            min_key = min(self.counter, key=self.counter.get)
            min_val = self.word_to_index[min_key]
            # print("Removing ", min_key, min_val)
            self.counter.pop(min_key, 'No Key found')
            self.word_to_index.pop(min_key, 'No Key found')
            self.index_to_word.pop(min_val, 'No Key found')
        self.counter[w] = 1
        token_index = len(self.word_to_index)+2 # Because of pad_value=0 and oov_value = 1
        # max_id = max(self.word_to_index, key=self.word_to_index.get)
        # token_index = self.word_to_index[max_id] + 1

        self.word_to_index[w] = token_index
        self.index_to_word[token_index] = w

    def __add_counter(self, w):
        if self.counter[w] >= 100000000:
            self.counter[w] = 100000000
        else:
            self.counter[w] = self.counter[w] + 1


    def words_to_seq(self, sentence):
        sequence = []
        for w in sentence:
            if w in self.word_to_index.keys():
                self.__add_counter(w)
                sequence.append(self.word_to_index[w])
            elif self.train:
                self.__insert_to_words(w)
                sequence.append(self.word_to_index[w])
            else:
                sequence.append(OOV_VALUE)
        return self.__pad_sequences(sequence)
        # return sequence

    def seq_to_words(self, sequence):
        sentence = []
        for s in sequence:
            if s == OOV_VALUE:
                sentence.append("OOV")
            elif s != PAD_VALUE:
                sentence.append(self.index_to_word[s])
        return sentence