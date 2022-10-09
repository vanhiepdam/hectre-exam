# -*- coding: utf-8 -*-
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from common.rest_framework.mixins import ProcessModelMixin
from harvest.serializers.v1.harvests.dashboard import GenerateDashboardResponseSerializerV1
from harvest.serializers.v1.harvests.dashboard import GenerateDashboardSerializerV1


class HarvestViewsetV1(
    GenericViewSet,
    ProcessModelMixin
):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='orchard_ids',
                description='Filter by orchards. '
                            'List of orchard ids separated by comma. Eg: abc,def',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='start_time',
                description='Start time to filter data. Format: YYYY-MM-DDTHH:MM:SSZ',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='end_time',
                description='End time to filter data. Format: YYYY-MM-DDTHH:MM:SSZ',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='metric',
                description='Metric for dashboard value. Choices: bin | cost',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='group_by',
                description='Dashboard data group by. Choices: variety | orchard',
                required=True,
                type=str
            ),
        ],
        responses={
            200: GenerateDashboardResponseSerializerV1(many=True)
        },
    )
    @action(
        detail=False,
        methods=['GET'],
        url_path='dashboard',
        url_name='dashboard',
        serializer_class=GenerateDashboardSerializerV1,
        pagination_class=None
    )
    def generate_dashboard(self, request, *args, **kwargs):
        return super().process_request_params(request, *args, **kwargs)
