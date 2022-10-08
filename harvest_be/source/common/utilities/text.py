import uuid
import string
import random
from hashlib import sha3_256

DEFAULT_RANDOM_TEXT = string.ascii_lowercase \
                      + string.ascii_uppercase \
                      + string.digits
DEFAULT_RANDOM_TEXT_UPPER_CASE = string.ascii_uppercase + string.digits
DEFAULT_RANDOM_NUMBERS = string.digits


class TextUtil(object):

    @classmethod
    def generate_uuid(cls):
        return str(uuid.uuid4())

    @classmethod
    def generate_random_text(cls, length=10, choices=DEFAULT_RANDOM_TEXT):
        return ''.join((random.choice(choices) for _ in range(length)))

    @classmethod
    def generate_random_text_upper_case(cls, length=10):
        return cls.generate_random_text(length=length, choices=DEFAULT_RANDOM_TEXT_UPPER_CASE)

    @classmethod
    def truncate_chars(cls, text, length=10, other='...', reserve=False):
        truncated_text = text[-length:] if reserve else text[:length]
        if len(text) > length:
            truncated_text = f"{other}{truncated_text}" if reserve else f"{truncated_text}{other}"
        return truncated_text

    @classmethod
    def generate_random_string_of_numbers(cls, length=10):
        return cls.generate_random_text(length=length, choices=DEFAULT_RANDOM_NUMBERS)

    @classmethod
    def hash_sha256(cls, text: str):
        return sha3_256(text.encode('utf-8')).hexdigest()
