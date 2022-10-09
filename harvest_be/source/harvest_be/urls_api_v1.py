# -*- coding: utf-8 -*-
from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include('harvest.urls.api_v1')),
]
