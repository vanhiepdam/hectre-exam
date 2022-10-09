# -*- coding: utf-8 -*-

import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from common.utilities.text import TextUtil
from harvest.models import Orchard


@factory.django.mute_signals(post_save)
class OrchardFactory(DjangoModelFactory):
    class Meta:
        model = Orchard
        django_get_or_create = ('id',)

    id = factory.LazyAttribute(lambda x: TextUtil.generate_uuid())
    name = factory.LazyAttribute(lambda x: TextUtil.generate_random_text(length=10))
