# -*- coding: utf-8 -*-
from django.db import models

from common.constants.text import LONG_TEXT
from common.constants.text import NORMAL_TEXT
from common.models.base import BaseModel


class Orchard(BaseModel):
    id = models.CharField(
        primary_key=True,
        max_length=NORMAL_TEXT
    )
    name = models.CharField(
        max_length=LONG_TEXT
    )
