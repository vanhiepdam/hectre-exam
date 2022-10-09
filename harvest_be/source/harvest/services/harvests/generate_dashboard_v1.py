# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List
from typing import Optional

from common.rest_framework.exceptions import BusinessLogicValidationError
from harvest.constants.harvest_dashboard import DashboardGroupBy
from harvest.constants.harvest_dashboard import DashboardMetric
from harvest.models import Orchard
from harvest.repositories.harvest import HarvestRepository


class GenerateDashboardServiceV1:
    def __init__(
            self,
            start_time: datetime,
            end_time: datetime,
            orchards: Optional[List[Orchard]],
            metric: str,
            group_by: str
    ) -> List:
        self.start_time = start_time
        self.end_time = end_time
        self.orchards = orchards
        self.metric = metric
        self.group_by = group_by

    def _validate(self):
        if self.metric not in DashboardMetric.values():
            raise BusinessLogicValidationError(f"{self.metric} is not supported.")
        if self.group_by not in DashboardGroupBy.values():
            raise BusinessLogicValidationError(f"{self.group_by} is not supported.")

    def generate(self):
        self._validate()
        data = HarvestRepository.aggregate_data_for_dashboard(
            start_time=self.start_time,
            end_time=self.end_time,
            orchards=self.orchards,
            group_by=self.group_by,
            metric=self.metric
        )
        return list(data)
