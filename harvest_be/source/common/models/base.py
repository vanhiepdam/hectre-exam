# -*- coding: utf-8 -*-

from common.constants.text import MEDIUM_TEXT
from common.utilities.text import TextUtil
from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def update_fields(self, **kwargs):
        self.__class__.objects.filter(pk=self.pk).update(**kwargs)


class BaseUUIDModel(BaseModel):
    id = models.UUIDField(
        default=TextUtil.generate_uuid,
        primary_key=True,
        unique=True,
    )

    class Meta:
        abstract = True


class ChangedAbstractModel(models.Model):
    changed_by = models.ForeignKey(
        to=User, related_name="%(app_label)s_%(class)s_changed",
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    changed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class StateHistoryAbstractModel(BaseModel, ChangedAbstractModel):
    old_value = models.CharField(max_length=MEDIUM_TEXT, blank=True, null=True)
    new_value = models.CharField(max_length=MEDIUM_TEXT)
    note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
