# -*- coding: utf-8 -*-
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from common.rest_framework.mixins import ProcessModelMixin
from harvest.serializers.v1.harvests.dashboard import DashboardSerializerV1


class HarvestViewsetV1(
    GenericViewSet,
    ProcessModelMixin
):
    @action(
        detail=False,
        methods=['GET'],
        url_path='dashboard',
        url_name='dashboard',
        serializer_class=DashboardSerializerV1
    )
    def get_dashboard(self, request, *args, **kwargs):
        return super().process_request_params(request, *args, **kwargs)
