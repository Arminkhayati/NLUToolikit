import random

ALPHABET = ["ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "ل", "م", "ن", "و", "ه", "ی",]
ALL_WORDS = [
    "معمولی", "شگفت انگیز", "اینترنت",
    "همراه اول", "ایرانسل", "رایتل", "شاتل", "خلیج فارس آنلاین",
    "تومن", "تومان", "تومانی", "تومنی", "ریال", "ریالی", "هزار", "هزاری", "میلیون", "میلیونی"
    , "میلیارد", "میلیاردی", "برای", "برا", "واس", "واسه", "سی",
    "من", "خودم", "م", "بنده", "مو", "خوم",
    "از", "با", "توسط", "بوسیله", "به وسیله",
    "بگیر", "بگیرید", "بگیرین", "میگیری", "میگیرید", "میگیرین"
    , "بخرید", "بخر", "بخرین", "میخرید", "میخرین", "میخری", "میخوام", "میخواستم", "بریز"
    , "کن", "بریزید", "بریزین", "کنید", "بکن", "بکنید", "بکنین", "کنین", "میکنی", "میکنین", "میکنید",
    "می کنی", "می کنین", "می کنید", "می خرید", "می خرین", "می خری", "می خوام", "می خواستم",  "می گیری",
    "می گیرید", "می گیرین", "لطفا", "خواهشا", "خواهشمندم", "تو رو خدا", "جان مادرت",
    "خواهش میکنم", "خواهش می کنم", "جان بچت", "ممنون میشم", "ممنون می شم", "جون دیت", "جون مادرت", "جون بچت",
    "موبایل", "تلفن", "تلفن همراه", "خط", "شماره", "شماره موبایل",
    "شماره تلفن", "شماره تلفن همراه", "شماره خط",
    "خط شماره", "موبایل شماره", "تلفن شماره", "تلفن همراه شماره", "گوشی",
    "کارت", "حساب", "شماره کارت", "شماره حساب", "کارت شماره", "حساب شماره",
    "برایم", "برام", "واسم", "واسهم", "سیم", "مبلغ", "کانتکم", "کانتکت", "مخاطب","مخاطبین"
    , "مخاطبینم", "کانتکتام", "<sos>", "<eos>", "شارژ", "یه",

]


def phone_number_generator():
    if random.random() < 0.5:
        a = random.randint(10000, 99999)
        b = random.randint(100000, 999999)
        return str(a) + str(b)
    else:
        words = random.randint(1, 3)
        name = ""
        first = True
        while(words>0):
            if not first:
                name = name + " "
            a = random.choices(ALPHABET, k=random.randint(3, 7))
            name = name + "".join(a)
            first = False
            words = words - 1
        return name

def bank_number_generator():
    if random.random() < 0.5:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
        c = random.randint(1000, 9999)
        d = random.randint(1000, 9999)
        return str(a) + str(b) + str(c) + str(d)
    else:
        words = random.randint(1, 3)
        name = ""
        first = True
        while(words>0):
            if not first:
                name = name + " "
            a = random.choices(ALPHABET, k=random.randint(3, 7))
            name = name + "".join(a)
            first = False
            words = words - 1
        return name

def charge_amount_generator():
    return str(random.randint(1, 10000000))

def charge_type_generator():
    values = ["معمولی", "شگفت انگیز", "اینترنت"]
    return random.choice(values)

def operator_generator():
    values = ["همراه اول", "ایرانسل", "رایتل", "شاتل", "خلیج فارس آنلاین"]
    return random.choice(values)

def unit_generator():
    values = ["تومن", "تومان", "تومانی", "تومنی", "ریال", "ریالی", "هزار", "هزاری", "میلیون", "میلیونی", "میلیارد", "میلیاردی"]
    return random.choice(values)

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
    values = ["بگیر", "بگیرید", "بگیرین", "میگیری", "میگیرید", "میگیرین"
        , "بخرید", "بخر", "بخرین", "میخرید", "میخرین", "میخری", "میخوام", "میخواستم", "بریز", "کن", "بریزید", "بریزین", "کنید", "بکن", "بکنید", "بکنین", "کنین", "میکنی", "میکنین", "میکنید",
              "می کنی", "می کنین", "می کنید", "می خرید", "می خرین", "می خری", "می خوام", "می خواستم",  "می گیری", "می گیرید", "می گیرین",]
    return random.choice(values)

def please_filler():
    values = ["لطفا", "خواهشا", "خواهشمندم", "تو رو خدا", "جان مادرت", "خواهش میکنم", "خواهش می کنم", "جان بچت", "ممنون میشم", "ممنون می شم", "جون دیت", "جون مادرت", "جون بچت"]
    return random.choice(values)

def device_filler():
    values = ["موبایل", "تلفن", "تلفن همراه", "خط", "شماره", "شماره موبایل",
              "شماره تلفن", "شماره تلفن همراه", "شماره خط",
              "خط شماره", "موبایل شماره", "تلفن شماره", "تلفن همراه شماره", "گوشی",
              "کانتکم", "کانتکت", "مخاطب","مخاطبین", "مخاطبینم", "کانتکتام"]
    return random.choice(values)

def account_filler():
    values = ["کارت", "حساب", "شماره کارت", "شماره حساب", "کارت شماره", "حساب شماره"]
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
    "device" : device_filler,
    "account" : account_filler
}
SLOT = {
    # Slots
    "charge_type": charge_type_generator,
    "bnumber": bank_number_generator,
    "pnumber": phone_number_generator,
    "amount": charge_amount_generator,
    "operator": operator_generator,
    "unit": unit_generator,
}

