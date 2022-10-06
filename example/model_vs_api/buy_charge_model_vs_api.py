from main.core.evaluation.single_sentence_prediction import get_predictor
from requests_toolbelt.multipart.encoder import MultipartEncoder
from sklearn.metrics import accuracy_score
from leven import levenshtein
import numpy as np
import argparse
import requests
import pickle
import uuid



parser = argparse.ArgumentParser(prog="dataset_evaluator", description='Evaluating model on input text (type "exit" to quit)')
parser.add_argument(
    '-s', '--sentence',
    type=str,
    default="برام شارژ بگیر",
    help='Your sample sentence.',
)

parser.add_argument(
    '-m', '--model',
    type=str,
    default="/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/model/full_model.h5",
    help='Path of model.',
)
parser.add_argument(
    '-xt', '--x-tokenizer',
    type=str,
    default='/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/data_dump/x_tokenizer.pickle',
    help='Path of X_Tokenizer pickle file.',
)
parser.add_argument(
    '-yt', '--y-tokenizer',
    type=str,
    default='/media/SSD1TB/khayati/projects/nlu/intent_slot_filling/output/data_dump/y_tokenizer.pickle',
    help='Path of Y_Tokenizer pickle file.',
)

parser.add_argument(
    '-bknd', '--backend',
    type=str,
    default="keras",
    help='Your model backend. (keras or pytorch) ...',
)

args = parser.parse_args().__dict__
# print(args)



labels_conv = {
    "Operatorname": "operator",
    "AMOUNT": "amount",
    "ORIGINACCOUNT": "bnumber",
    "MOBILENUMBER": "pnumber",
    "chargeType": "charge_type",
}

labels_conv_inv = {
    "operator": "Operatorname",
    "amount": "AMOUNT",
    "bnumber": "ORIGINACCOUNT",
    "pnumber": "MOBILENUMBER",
    "charge_type": "chargeType",
}
slots_order = ["bnumber", "pnumber", "amount", "operator", "charge_type"]

def create_grand_truth(sentence, slots):
    grand_truth = []
    for i, slot in enumerate(slots):
        if slot != "O":
            grand_truth.append((sentence[i], slot))
    return grand_truth

def concat_operator_post(words, slots, word):
    result_word = word
    for i, slot in enumerate(slots):
        if slot == "operator_post":
            result_word = result_word + " " + words[i]
        else:
            break
    return result_word, "operator"

def concat_bnumber_post(words, slots, word):
    result_word = word
    for i, slot in enumerate(slots):
        if slot == "bnumber_post":
            result_word = result_word + " " + words[i]
        else:
            break
    return result_word, "bnumber"

def concat_pnumber_post(words, slots, word):
    result_word = word
    for i, slot in enumerate(slots):
        if slot == "pnumber_post":
            result_word = result_word + " " + words[i]
        else:
            break
    return result_word, "pnumber"

def concat_charge_type_post(words, slots, word):
    result_word = word
    for i, slot in enumerate(slots):
        if slot == "charge_type_post":
            result_word = result_word + " " + words[i]
        else:
            break
    return result_word, "charge_type"

def concat_post(grand_truth):
    words, slots = [ i for i, j in grand_truth ], [ j for i, j in grand_truth ]
    new_words, new_slots = [], []
    for i, slot in enumerate(slots):
        if slot == "operator":
            w, s = concat_operator_post(words[i+1:], slots[i+1:], words[i])
            new_words.append(w)
            new_slots.append(s)
        elif slot == "bnumber":
            w, s = concat_bnumber_post(words[i+1:], slots[i+1:], words[i])
            new_words.append(w)
            new_slots.append(s)
        elif slot == "pnumber":
            w, s = concat_pnumber_post(words[i+1:], slots[i+1:], words[i])
            new_words.append(w)
            new_slots.append(s)
        elif slot == "charge_type":
            w, s = concat_charge_type_post(words[i+1:], slots[i+1:], words[i])
            new_words.append(w)
            new_slots.append(s)
        elif "_post" not in slot:
            new_words.append(words[i])
            new_slots.append(slots[i])
    return new_words, new_slots

def create_prediction(gt, pred):
    prediction_list, grand_truth_list = [], []
    prediction_dict, grand_truth_dict = {}, {}
    for k in gt.keys():
        if k == "unit":
            continue
        grand_truth_dict[k] = gt[k]
        if (k not in pred.keys()) or (pred[k] == None):
            prediction_dict[k] = "----"
            prediction_list.append("----")
        else:
            prediction_dict[k] = pred[k]
            prediction_list.append(pred[k])
        grand_truth_list.append(gt[k])

    return grand_truth_list, prediction_list, grand_truth_dict, prediction_dict

def create_api_prediction(gt, pred):
    pred_dict = {}
    for p in pred:
        pred_dict[p["name"]] = p["value"]

    if ("unit" in gt.keys()):
        if "توم" in gt["unit"]:
            gt["amount"] = gt["amount"] + "0"
    prediction_list, grand_truth_list = [], []
    prediction_dict, grand_truth_dict = {}, {}
    for k in gt.keys():
        if k == "unit":
            continue
        pred_key = labels_conv_inv[k]
        grand_truth_dict[k] = gt[k]
        if (pred_key not in pred_dict.keys()) or (pred_dict[pred_key] == None):
            prediction_dict[k] = "----"
            prediction_list.append("----")
        else:
            prediction_dict[k] = pred_dict[pred_key]
            prediction_list.append(pred_dict[pred_key])
        grand_truth_list.append(gt[k])
    return grand_truth_list, prediction_list, grand_truth_dict, prediction_dict

def create_slot_sequence(yy, yy_pred):
    sequence = ""
    for o in slots_order:
        if o not in yy.keys():
            continue
        if (o == "charge_type") and (yy_pred[o] == "1"):
            yy_pred[o] = "معمولی"
        if yy[o] == yy_pred[o]:
            sequence = sequence + "a"
        else:
            sequence = sequence + "b"
    return sequence
############################Test Api###############################################
with open("data/data.pickle", 'rb') as f:
    data = pickle.load(f)

from_, to_ = 0, 2000
grand_truths = []
for sentence, slots in zip(data["x"], data["y"]):
    gt = create_grand_truth(sentence, slots)
    new_words, new_slots = concat_post(gt)
    grand_truths.append(dict(list(zip(new_slots, new_words))))

api_url = "https://api.msgata.com/nlu"
outputs = []

for i, sentence in enumerate(data["x"][from_: to_]):
    sentence = " ".join(sentence)
    mp_encoder = MultipartEncoder(fields={'text': sentence, "language": "fa", "userId": str(uuid.uuid4())})
    headers = {'Content-Type': mp_encoder.content_type, "devkey": "397124958FA659C9F1A5C7BC96788",
               "token": "12", "Cache-Control": "no-cache",
               "Pragma": "no-cache"}
    res = requests.post(api_url, data=mp_encoder, headers=headers)
    js = res.json()
    result = js['Response']['responses'][0]['entities']
    # print(result)
    y, y_pred, yy, yy_pred = create_api_prediction(grand_truths[i], result)
    outputs.append((y, y_pred, yy, yy_pred))

# with open("output_txt/output.pickle", "wb") as f:
#     pickle.dump(outputs, f)

# with open("output_txt/output.pickle", "rb") as f:
#     outputs = pickle.load(f)

sequences = map(lambda item: create_slot_sequence(item[2], item[3]), outputs)
sequences = list(sequences)
result = []
for s in sequences:
    orig = "a" * len(s)
    metric = levenshtein(orig, s)
    result.append(metric)

print("Levenshtein Score for API Result vs Ground Truth: " , np.sum(result))


############################Test Model###############################################
predictor = get_predictor(args)
grand_truths = []
for sentence, slots in zip(data["x"], data["y"]):
    gt = create_grand_truth(sentence, slots)
    new_words, new_slots = concat_post(gt)
    grand_truths.append(dict(list(zip(new_slots, new_words))))


outputs = []
for i, sentence in enumerate(data["x"][from_: to_]):
  _, slots = predictor(" ".join(sentence))
  pred = create_grand_truth(sentence, slots)
  new_words, new_slots = concat_post(pred)
  output = create_prediction(grand_truths[i], dict(list(zip(new_slots, new_words))))
  outputs.append(output)

sequences = map(lambda item: create_slot_sequence(item[2], item[3]), outputs)
sequences = list(sequences)

result = []
for s in sequences:
    orig = "a" * len(s)
    metric = levenshtein(orig, s)
    result.append(metric)
print("Levenshtein Score for Model Result vs Ground Truth: " , np.sum(result))



##########################################3