# -*- coding: utf-8 -*-
from django.db import models

from common.models.base import BaseUUIDModel
from user.models import User


class Harvest(BaseUUIDModel):
    user = models.ForeignKey(
        User,
        related_name='harvests',
        on_delete=models.PROTECT,
    )
    orchard = models.ForeignKey(
        'harvest.Orchard',
        related_name='harvests',
        on_delete=models.PROTECT
    )
    variety = models.ForeignKey(
        'harvest.Variety',
        related_name='harvests',
        on_delete=models.PROTECT
    )
    hours_worked = models.DecimalField(max_digits=10, decimal_places=1)
    picking_time = models.DateTimeField()
    number_of_bins = models.PositiveIntegerField()
    pay_rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
