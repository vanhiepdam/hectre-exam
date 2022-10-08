# -*- coding: utf-8 -*-
from abc import abstractmethod

from django.contrib.auth.models import User
from django.db import models
from django.utils.module_loading import import_string

from common.models.state_mixins import ModelStateMixin
from common.more_constants.text import MEDIUM_TEXT, LONG_TEXT
from common.utilities.text import TextUtil


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


class PipelineTrackerAbstractModel(BaseModel, ModelStateMixin):
    step = models.CharField(
        max_length=LONG_TEXT, null=False, blank=False
    )
    extra_data = models.JSONField(default=dict, blank=True)
    note = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    @abstractmethod
    def tracker_owner(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    def _load_step_class(self):
        return import_string(self.step)

    def _load_step_instance(self):
        step_class = self._load_step_class()
        step_instance = step_class(instance=self.tracker_owner)
        return step_instance
