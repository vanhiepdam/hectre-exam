import random
from decimal import Decimal


class NumberUtil:

    @classmethod
    def to_decimal(cls, value):
        return Decimal(str(value))

    @classmethod
    def generate_random_number(cls, _from: int, _to: int):
        return random.randint(_from, _to)