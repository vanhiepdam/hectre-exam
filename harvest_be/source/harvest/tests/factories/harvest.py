# -*- coding: utf-8 -*-
from decimal import Decimal

import factory
from django.db.models.signals import post_save
from django.utils import timezone
from factory.django import DjangoModelFactory

from common.utilities.number import NumberUtil
from harvest.models import Harvest
from harvest.tests.factories.orchard import OrchardFactory
from harvest.tests.factories.variety import VarietyFactory
from user.tests.factories.user import UserFactory


@factory.django.mute_signals(post_save)
class HarvestFactory(DjangoModelFactory):
    class Meta:
        model = Harvest

    user = factory.SubFactory(UserFactory)
    orchard = factory.SubFactory(OrchardFactory)
    variety = factory.SubFactory(VarietyFactory)
    hours_worked = factory.LazyAttribute(
        lambda x: Decimal(NumberUtil.generate_random_number(1, 1000))
    )
    number_of_bins = factory.LazyAttribute(
        lambda x: NumberUtil.generate_random_number(1, 1000)
    )
    pay_rate_per_hour = factory.LazyAttribute(
        lambda x: Decimal(NumberUtil.generate_random_number(20, 100))
    )
    picking_time = factory.LazyAttribute(lambda x: timezone.now())
