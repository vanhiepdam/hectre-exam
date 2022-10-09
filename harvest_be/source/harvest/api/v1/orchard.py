# -*- coding: utf-8 -*-
from rest_framework import filters
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from harvest.repositories.orchard import OrchardRepository
from harvest.serializers.v1.orchards.list import ListOrchardSerializerV1


class OrchardViewsetV1(
    GenericViewSet,
    ListModelMixin
):
    permission_classes = [AllowAny]
    queryset = OrchardRepository.get_all()
    serializer_class = ListOrchardSerializerV1
    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = [
        'id',
        'name',
    ]
