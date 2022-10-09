# -*- coding: utf-8 -*-
from common.constants.enum import ConstantEnum


class DashboardMetric(str, ConstantEnum):
    BIN = 'bin'
    COST = 'cost'


class DashboardGroupBy(str, ConstantEnum):
    VARIETY = 'variety'
    ORCHARD = 'orchard'
