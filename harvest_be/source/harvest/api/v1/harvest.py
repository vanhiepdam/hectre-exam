# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from common.rest_framework.mixins import ProcessModelMixin
from harvest.serializers.v1.harvests.dashboard import GenerateDashboardSerializerV1


class HarvestViewsetV1(
    GenericViewSet,
    ProcessModelMixin
):
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=['GET'],
        url_path='dashboard',
        url_name='dashboard',
        serializer_class=GenerateDashboardSerializerV1
    )
    def generate_dashboard(self, request, *args, **kwargs):
        return super().process_request_params(request, *args, **kwargs)
