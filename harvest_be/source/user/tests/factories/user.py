# -*- coding: utf-8 -*-

import factory
from django.db.models.signals import post_save
from factory.django import DjangoModelFactory

from common.utilities.text import TextUtil
from user.models import User


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('id',)

    id = factory.LazyAttribute(lambda x: TextUtil.generate_uuid())
    username = factory.LazyAttribute(lambda x: TextUtil.generate_random_text(length=10))
