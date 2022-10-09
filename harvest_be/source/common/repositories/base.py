import abc
from typing import Optional, Union
from typing import Union


class BaseRepository:
    @property
    @abc.abstractmethod
    def model(self):
        pass

    @classmethod
    def _apply_query_optimization(cls, queryset, **kwargs):
        only_fields = kwargs.get('only_fields', [])
        defer_fields = kwargs.get('defer_fields', [])
        select_related_fields = kwargs.get('select_related_fields', [])
        prefetch_related_fields = kwargs.get('prefetch_related_fields', [])
        order_by_fields = kwargs.get('order_by_fields', [])
        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)
        if only_fields:
            queryset = queryset.only(*only_fields)
        if defer_fields:
            queryset = queryset.defer(*defer_fields)
        if order_by_fields:
            queryset = queryset.order_by(*order_by_fields)
        return queryset

    @classmethod
    def get_or_create(cls, defaults=None, **kwargs):
        return cls.model.objects.get_or_create(defaults=defaults, **kwargs)

    @classmethod
    def get_all(cls, **kwargs):
        queryset = cls.model.objects.all()
        queryset = cls._apply_query_optimization(queryset, **kwargs)
        return queryset

    @classmethod
    def get_by_pk(cls, object_pk: Optional[Union[int, str]]):
        return cls.model.objects.get(pk=object_pk)

    @classmethod
    def get_by_id(cls, object_id: Union[int, str]):
        return cls.model.objects.get(id=object_id)

    @classmethod
    def find_by_id(cls, object_id: Union[int, str]):
        return cls.model.objects.filter(id=object_id).first()

    @classmethod
    def find_by_list_of_ids(cls, object_ids: Union[int, str]):
        return cls.model.objects.filter(id__in=object_ids)

    @classmethod
    def create_object(cls, **data):
        return cls.model.objects.create(**data)

    @classmethod
    def get_first(cls, order_by='pk'):
        return cls.model.objects.order_by(order_by).last()

    @classmethod
    def get_last(cls, order_by='pk'):
        return cls.model.objects.order_by(order_by).last()

    @classmethod
    def count(cls, **condition):
        return cls.model.objects.filter(**condition).count()
