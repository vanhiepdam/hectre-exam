# -*- coding: utf-8 -*-
from enum import Enum


class ConstantEnum(Enum):
    @classmethod
    def get_choices(cls):
        return [(tag.value, tag.name) for tag in cls]
