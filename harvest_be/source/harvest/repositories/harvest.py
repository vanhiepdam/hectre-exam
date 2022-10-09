# -*- coding: utf-8 -*-
import datetime
from typing import Iterable
from typing import Optional
from typing import Union

from django.db.models import F
from django.db.models import QuerySet
from django.db.models import Sum

from common.repositories.base import BaseRepository
from harvest.constants.harvest_dashboard import DashboardGroupBy
from harvest.constants.harvest_dashboard import DashboardMetric
from harvest.models import Harvest
from harvest.models import Orchard


class HarvestRepository(BaseRepository):
    model = Harvest

    @classmethod
    def find_raw_data_for_dashboard(
            cls,
            start_time: datetime,
            end_time: datetime,
            orchards: Optional[Iterable[Orchard]]
    ) -> QuerySet:
        queryset = cls.model.objects.filter(
            picking_time__gte=start_time,
            picking_time__lte=end_time,
        )

        if orchards is not None:
            queryset = queryset.filter(
                orchard__in=orchards
            )

        queryset = queryset.select_related(
            'user',
            'orchard',
            'variety',
        )
        return queryset

    @classmethod
    def aggregate_data_for_dashboard(
            cls,
            start_time: datetime,
            end_time: datetime,
            orchards: Optional[Iterable[Orchard]],
            group_by: Union[str, DashboardGroupBy],
            metric: Union[str, DashboardMetric]
    ) -> QuerySet:
        raw_data = cls.find_raw_data_for_dashboard(
            start_time=start_time,
            end_time=end_time,
            orchards=orchards,
        )

        # set aggregate metric
        if metric == DashboardMetric.BIN:
            aggregate_metric = 'number_of_bins'
        elif metric == DashboardMetric.COST:
            aggregate_metric = F('hours_worked') * F('pay_rate_per_hour')
        else:
            aggregate_metric = metric

        data = raw_data.values(gid=F(f'{group_by}__id'), name=F(f'{group_by}__name')).annotate(
            value=Sum(aggregate_metric)
        )
        return data
