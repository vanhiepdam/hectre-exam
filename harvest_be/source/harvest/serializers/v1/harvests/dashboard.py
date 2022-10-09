# -*- coding: utf-8 -*-
from rest_framework import serializers

from common.rest_framework.serializers import ProcessSerializer
from harvest.constants.harvest_dashboard import DashboardGroupBy
from harvest.constants.harvest_dashboard import DashboardMetric
from harvest.repositories.orchard import OrchardRepository
from harvest.services.harvests.generate_dashboard_v1 import GenerateDashboardServiceV1


class GenerateDashboardSerializerV1(ProcessSerializer):
    orchard_ids = serializers.CharField(allow_blank=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    metric = serializers.ChoiceField(choices=DashboardMetric.get_choices())
    group_by = serializers.ChoiceField(choices=DashboardGroupBy.get_choices())

    def validate_orchard_ids(self, value):
        if value:
            return value.split(',')
        return None

    def process(self, request, validated_data):
        orchard_ids = validated_data['orchard_ids']
        if orchard_ids:
            orchards = OrchardRepository.find_by_list_of_ids(object_ids=orchard_ids)
        else:
            orchards = None

        service = GenerateDashboardServiceV1(
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            orchards=orchards,
            metric=validated_data['metric'],
            group_by=validated_data['group_by']
        )
        result = service.generate()
        return result
