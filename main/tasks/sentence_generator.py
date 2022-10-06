import re


class SentenceGenerator:
    def __init__(self, placeholder_filler_fn):
        self.placeholder_filler_fn = placeholder_filler_fn

    def __check_placeholder(self, w):
        if "}" in w:
            if "for_{me}" in w:
                s1, sv1 = self.placeholder_filler_fn("for")
                s2, sv2 = self.placeholder_filler_fn("me")
                sv = sv1[0] + sv2[0]
                # check for برایم or برای من
                if len(sv.split(" ")) > 1:
                    return ["O", "O"], [sv1[0], sv2[0].strip()]
                else:
                    return ["O"], [sv]
            else:
                placeholder = re.findall("\{(.*?)\}", w)[0]
                return self.placeholder_filler_fn(placeholder)
        elif w == "<sos>":
            return (["<sos>"], [w])
        elif w == "<eos>":
            return (["<eos>"], [w])
        else:
            return (["O"], [w])

    def __check_for_post(self, slot, sent):
        new_slot, new_sent = [], []
        for i in range(len(sent)):
            new_sl, new_se = slot[i], sent[i]
            # new_se = str(new_se)
            if new_sl == "O":
                for w in new_se.split(" "):
                    new_slot.append(new_sl)
                    new_sent.append(w)
            else:
                words = new_se.split(" ")
                new_slot.append(new_sl)
                new_sent.append(words.pop(0))
                for w in words:
                    new_slot.append(new_sl + "_post")
                    new_sent.append(w)
        return new_slot, new_sent

    def generate_from(self, template):
        sentence = []
        slots = []
        for w in template:
            if (w == '') or (w == ' '):
                continue
            slot, sent = self.__check_placeholder(w)
            slot, sent = self.__check_for_post(slot, sent)
            sentence = sentence + sent
            slots = slots + slot
        return sentence, slots