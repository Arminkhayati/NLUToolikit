import random

ALPHABET = ["ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "ل", "م", "ن", "و", "ه", "ی",]
ALL_WORDS = [
    ####
    "برای", "برا", "واس", "واسه", "سی",
    ####
    "من", "خودم", "م", "بنده", "مو", "خوم",
    ####
    "از", "با", "توسط", "بوسیله", "به وسیله",
    ####
    "میخوام", "میخواستم", "می خوام", "می خواستم", "میخوایم", "میخواید",
    "می خوایم", "می خواید", "میخواستیم", "می خواستیم", "قصد دارم", "قصد داریم", "قصدش داریم",
    ####
    "بگیر", "بگیرید", "بگیرین", "میگیری", "میگیرید", "میگیرین", "بگیرم", "بگیرن",
    "می گیری", "می گیرید", "می گیرین", "بگیریم",
    ####
    "بخرید", "بخر", "بخرین", "میخرید", "میخرین", "میخری", "بخریم", "بخرم", "بخری" ,
    "می خرید", "می خرین", "می خری",
    ####
    "میخوام", "میخواستم", "می خوام", "می خواستم", "میخوایم", "میخواید", "می خوایم", "می خواید",
    "میخواستیم", "می خواستیم",
    ####
    "بریزید", "بریزین",
    "رزرو","شارژ", "بوک", "نگه داری", "ست",
    ####
    "کنید", "بکن", "بکنید", "بکنین", "بکنم", "بکنیم", "میکنین", "کنم", "کنی",
    ####
    "کنین", "میکنی", "میکنین", "میکنید", "می کنی", "می کنین", "می کنید", "کن",
    ####
    ####
    "لطفا", "خواهشا", "خواهشمندم", "تو رو خدا", "جان مادرت",
    "خواهش میکنم", "خواهش می کنم", "جان بچت", "ممنون میشم", "ممنون می شم", "جون دیت", "جون مادرت", "جون بچت",
    ####
    "برایم", "برام", "واسم", "واسهم", "سیم",
    ####
    "نفر", "نفره", "نفرات", "بزرگسال", "بزرگ سال", "بچه", "بچه سال",
    "کودک", "دختر بچه", "پسر بچه", "آقا", "خانم", "مرد", "زن", "نوزاد", "لیدی", "جنتلمن", "خوابه", "خواب"
    ####
    "<sos>", "<eos>", "یه", "اتاق", "هتل", "شهر",  "تا",


]



######################SLOTS#######################

def num_room_generator():
    return str(random.randint(1, 50))

def time_generator():
    return str(random.randint(1, 50))

def time_unit_generator():
    values = ["روز", "شب", "هفته", "ماه", "سال", "ساعت"]
    return random.choice(values)

def num_bed_generator():
    return str(random.randint(1, 20))

def num_person_generator():
    return str(random.randint(1, 100))

def person_unit_generator():
    values = ["نفر", "نفره", "نفرات", "بزرگسال", "بزرگ سال", "بچه", "بچه سال",
              "کودک", "دختر بچه", "پسر بچه", "آقا", "خانم", "مرد", "زن", "نوزاد", "لیدی", "جنتلمن", "خوابه", "خواب"]
    return random.choice(values)

def hotel_name_generator():
    words = random.randint(1, 6)
    name = ""
    first = True
    while(words>0):
        if not first:
            name = name + " "
        a = random.choices(ALPHABET, k=random.randint(2, 10))
        name = name + "".join(a)
        first = False
        words = words - 1
    return name

def hotel_city_generator():
    words = random.randint(1, 4)
    name = ""
    first = True
    while(words>0):
        if not first:
            name = name + " "
        a = random.choices(ALPHABET, k=random.randint(2, 10))
        name = name + "".join(a)
        first = False
        words = words - 1
    return name


######################WORD FILLER#######################
def for_filler():
    values = ["برای", "برا", "واس", "واسه", "سی", ]
    return random.choice(values)

def me_filler():
    values = ["من", "خودم", "م", "بنده", "مو", "خوم"]
    a = random.choice(values)
    if a != "م":
        a = " " + a
    return a

def from_filler():
    values = ["از", "با", "توسط", "بوسیله", "به وسیله"]
    return random.choice(values)

def verb_filler():

    verb = ""
    pre_pre_values = ["میخوام", "میخواستم", "می خوام", "می خواستم", "میخوایم", "میخواید"
        , "می خوایم", "می خواید", "میخواستیم", "می خواستیم", "قصد دارم", "قصد داریم", "قصدش داریم",
        ]
    pre_values = ["رزرو","شارژ", "بوک", "نگه داری", "ست",]
    values = [
        ####
        "بگیر", "بگیرید", "بگیرین", "میگیری", "میگیرید", "میگیرین", "بگیرم", "بگیرن",
        "می گیری", "می گیرید", "می گیرین", "بگیریم",
        ####
         "بخرید", "بخر", "بخرین", "میخرید", "میخرین", "میخری", "بخریم", "بخرم", "بخری" ,
              "می خرید", "می خرین", "می خری",
        ####
              "میخوام", "میخواستم", "می خوام", "می خواستم", "میخوایم", "میخواید", "می خوایم", "می خواید",
              "میخواستیم", "می خواستیم"
        ####
              "بریز", "بریزید", "بریزین",
        ####
              "کنید", "بکن", "بکنید", "بکنین", "بکنم", "بکنیم", "میکنین", "کنم", "کنی",
        ####
              "کنین", "میکنی", "میکنین", "میکنید", "می کنی", "می کنین", "می کنید", "کن",
        ####
              "تهیه کن", "تهیه کنیم", "تهیه کنم", "تهیه بکنیم", "تهیه بکنم", "تهیه بکن",
              ]

    if random.random() > 0.5:
        verb = verb + random.choice(pre_pre_values) + " "
    if random.random() > 0.5:
        verb = verb + random.choice(pre_values) + " "
    verb = verb + random.choice(values)
    return verb

def please_filler():
    values = ["لطفا", "خواهشا", "خواهشمندم", "تو رو خدا", "جان مادرت", "خواهش میکنم", "خواهش می کنم", "جان بچت", "ممنون میشم", "ممنون می شم", "جون دیت", "جون مادرت", "جون بچت"]
    return random.choice(values)

def in_filler():
    values = ["در", "تو", "داخل", "توی", "از", "درون"]
    return random.choice(values)

def bed_unit_filler():
    values = ["تخت", "تخته"]
    return random.choice(values)


def get_word_or_slot_value(w):
    if w in WORD_FILLER.keys():
        return ["O"], [WORD_FILLER[w]()]
    else:
        return [w], [SLOT[w]()]

def is_slot(w):
    if w in SLOT.keys():
        return True
    else:
        return False

def get_all_words():
    all_words = []
    for words in ALL_WORDS:
        for w in words.split(" "):
            all_words.append(w)
    all_words = list(set(all_words))
    return sorted(all_words)

WORD_FILLER = {
    # Word Filling
    "for": for_filler,
    "me": me_filler,
    "from": from_filler,
    "verb": verb_filler,
    "please": please_filler,
    "in": in_filler,
    "bed_unit": bed_unit_filler,
}

SLOT = {
    # Slots
    "num_room":         num_room_generator,
    "time":             time_generator,
    "time_unit":        time_unit_generator,
    "num_bed":          num_bed_generator,
    "num_person":       num_person_generator,
    "person_unit":      person_unit_generator,
    "hotel_name":       hotel_name_generator,
    "hotel_city":       hotel_city_generator,
}

# slots: num_room, time, time_unit, num_bed, num_person, person_unit, hotel_name, hotel_city,
# slots: person_unit_post, hotel_name_post, hotel_city_post
# Fillers: for, me, for_me, from, verb, please, in, bed_unit