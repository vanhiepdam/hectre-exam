from abc import abstractmethod
from rest_framework import serializers


class AbstractProcessSerializer(serializers.Serializer):

    def create(self, validated_data):
        raise Exception("No support Create")

    def update(self, instance, validated_data):
        raise Exception("No support Update")


class ProcessSerializer(AbstractProcessSerializer):
    @abstractmethod
    def process(self, request, validated_data):
        raise Exception("Please implement method process()")


class ProcessObjectSerializer(AbstractProcessSerializer):

    @abstractmethod
    def process_object(self, request, instance, validated_data):
        raise Exception("Please implement method process_object()")
