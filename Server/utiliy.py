import hashlib
from itertools import chain, repeat
import re
import pytz
from datetime import datetime

def has_special_characters(s):
    return re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(s)

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def datetime_now():
    return datetime.now(tz=pytz.UTC)


def ask_and_wait_valid_answer(list_possible, question):
    prompts = chain([question], repeat("Not valid, please try again: "))
    replies = map(input, prompts)
    lowercased_replies = map(str.lower, replies)
    stripped_replies = map(str.strip, lowercased_replies)
    valid_response = next(filter(list_possible.__contains__, stripped_replies))
    return valid_response


def ask_and_wait_pos_integer(question):
    prompts = chain([question], repeat("Not valid, please try again: "))
    replies = map(input, prompts)
    numeric_strings = filter(str.isnumeric, replies)
    numbers = map(int, numeric_strings)
    is_positive = (0.).__lt__
    valid_response = next(filter(is_positive, numbers))
    return valid_response


def get_ingame_input_artis():
    return ["BOOK_OF_BASAN", "LIGHT_OF_EGGENDIL", "TACHYON_DEFLECTOR", "SHIP_IN_A_BOTTLE", "TITANIUM_ACTUATOR",
            "DILITHIUM_MONOCLE", "QUANTUM_METRONOME", "PHOENIX_FEATHER", "THE_CHALICE", "INTERSTELLAR_COMPASS",
            "CARVED_RAINSTICK", "BEAK_OF_MIDAS", "MERCURYS_LENS", "NEODYMIUM_MEDALLION", "ORNATE_GUSSET",
            "TUNGSTEN_ANKH", "AURELIAN_BROOCH", "VIAL_MARTIAN_DUST", "DEMETERS_NECKLACE", "LUNAR_TOTEM",
            "PUZZLE_CUBE"], ["bob", "light", "deflector", "siab", "actuator", "monocle", "metronome", "feather",
                             "chalice",
                             "compass", "rainstick", "beak", "lens", "medallion", "gusset", "ankh", "brooch", "vial",
                             "necklace", "totem", "cube"]


def get_leaderboards_names_static():
    return ['terra', 'tachyon', 'shell', 'bob', 'light', 'deflector', 'siab', 'actuator', 'monocle', 'metronome',
            'feather', 'chalice', 'compass', 'rainstick', 'beak', 'lens', 'medallion', 'gusset', 'ankh', 'brooch',
            'vial', 'necklace', 'totem', 'cube', 'gold', 'tau', 'titanium', 'clarity', 'lunar', 'prophecy', 'life',
            'quantum', 'dilithium', 'soul']

