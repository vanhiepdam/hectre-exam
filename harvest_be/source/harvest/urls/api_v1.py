# -*- coding: utf-8 -*-
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from harvest.api.v1.harvest import HarvestViewsetV1
from harvest.api.v1.orchard import OrchardViewsetV1

router = DefaultRouter()

router.register(
    prefix=r'harvests',
    viewset=HarvestViewsetV1,
    basename='harvest-model-viewset-v1'
)
router.register(
    prefix=r'orchards',
    viewset=OrchardViewsetV1,
    basename='orchard-model-viewset-v1'
)

urlpatterns = [
    # path('', include(router.urls)),
]
