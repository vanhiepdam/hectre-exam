# -*- coding: utf-8 -*-
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from harvest.api.v1.harvest import HarvestViewsetV1

router = DefaultRouter()

router.register(
    prefix=r'harvests',
    viewset=HarvestViewsetV1,
    basename='harvest-model-viewset-v1'
)

urlpatterns = [
    path('', include(router.urls)),
]
