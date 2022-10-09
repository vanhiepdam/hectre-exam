# -*- coding: utf-8 -*-
from rest_framework import serializers

from harvest.models import Orchard


class ListOrchardSerializerV1(serializers.ModelSerializer):
    class Meta:
        fields = [
            'id',
            'name',
        ]
        model = Orchard
