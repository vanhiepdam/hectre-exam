from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response


class ProcessModelMixin:
    """
    Create a model instance.
    """

    @staticmethod
    def _get_response(data, http_status=status.HTTP_200_OK):
        data = data if data is not None else {'data': 'OK'}
        return Response(data, status=http_status)

    def process(self, request, *args, **kwargs):
        """
        data passed to serializer will be retrieved from body request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = serializer.process(request, serializer.validated_data)
        except DjangoValidationError as ex:
            raise DRFValidationError(ex.message)
        return self._get_response(data)

    def process_object(self, request, *args, **kwargs):
        """"
        data passed to serializer will be retrieved from body request
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            data = serializer.process_object(
                request, instance, serializer.validated_data
            )
        except DjangoValidationError as ex:
            raise DRFValidationError(ex.message)
        return self._get_response(data)

    def process_request_params(self, request, *args, **kwargs):
        """"
        data passed to serializer will be retrieved from url request
        """
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.process(request, serializer.validated_data)
        return self._get_response(data)


class ManuallyPaginateResponseMixin:
    def generate_paginated_response(self, queryset):
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
