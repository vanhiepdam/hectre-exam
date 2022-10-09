# -*- coding: utf-8 -*-
from common.rest_framework.serializers import ProcessSerializer


class DashboardSerializerV1(ProcessSerializer):
    def process(self, request, validated_data):
        pass
