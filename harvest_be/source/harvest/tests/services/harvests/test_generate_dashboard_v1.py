# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

import pytest

from common.rest_framework.exceptions import BusinessLogicValidationError
from harvest.services.harvests.generate_dashboard_v1 import GenerateDashboardServiceV1

pytestmark = pytest.mark.django_db


def test_failure__metric_is_not_valid(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'wrong_metric'
    group_by = 'variety'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action & assert
    with pytest.raises(BusinessLogicValidationError):
        service.generate()


def test_failure__group_by_is_not_valid(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'wrong_group_by'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action & assert
    with pytest.raises(BusinessLogicValidationError):
        service.generate()


def test_success__query_all_data__metric_bin__group_by_variety(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'variety'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action
    data = service.generate()

    # assert
    assert len(data) == 3

    # assert pink lady data
    pink_lady_data = [
        item for item in data
        if item['name'] == 'Pink Lady'
    ]
    assert len(pink_lady_data) == 1
    pink_lady_data = pink_lady_data[0]
    assert pink_lady_data['value'] == 16

    # assert galaxy data
    galaxy_data = [
        item for item in data
        if item['name'] == 'Galaxy'
    ]
    assert len(galaxy_data) == 1
    galaxy_data = galaxy_data[0]
    assert galaxy_data['value'] == 20

    # assert royal gala data
    royal_gala_data = [
        item for item in data
        if item['name'] == 'Royal Gala'
    ]
    assert len(royal_gala_data) == 1
    royal_gala_data = royal_gala_data[0]
    assert royal_gala_data['value'] == 11


def test_success__query_all_data__metric_cost__group_by_variety(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'cost'
    group_by = 'variety'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action
    data = service.generate()

    # assert
    assert len(data) == 3

    # assert pink lady data
    pink_lady_data = [
        item for item in data
        if item['name'] == 'Pink Lady'
    ]
    assert len(pink_lady_data) == 1
    pink_lady_data = pink_lady_data[0]
    assert pink_lady_data['value'] == Decimal("42.36") * Decimal("7.9")

    # assert galaxy data
    galaxy_data = [
        item for item in data
        if item['name'] == 'Galaxy'
    ]
    assert len(galaxy_data) == 1
    galaxy_data = galaxy_data[0]
    assert galaxy_data['value'] == (
            Decimal("76.63") * Decimal("1.4") +
            Decimal("70.09") * Decimal("6.1") +
            Decimal("42.67") * Decimal("6.4")
    )

    # assert royal gala data
    royal_gala_data = [
        item for item in data
        if item['name'] == 'Royal Gala'
    ]
    assert len(royal_gala_data) == 1
    royal_gala_data = royal_gala_data[0]
    assert royal_gala_data['value'] == (
            Decimal("45.15") * Decimal("5.7")
    )


def test_success__query_all_data__metric_cost__group_by_orchard(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'cost'
    group_by = 'orchard'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action
    data = service.generate()

    # assert
    assert len(data) == 2

    # assert cypress data
    cypress_data = [
        item for item in data
        if item['name'] == 'Cypress'
    ]
    assert len(cypress_data) == 1
    cypress_data = cypress_data[0]
    assert cypress_data['value'] == (
            Decimal("42.36") * Decimal("7.9") +
            Decimal("70.09") * Decimal("6.1") +
            Decimal("76.63") * Decimal("1.4") +
            Decimal("42.67") * Decimal("6.4")
    )

    # assert benner road data
    benner_road_data = [
        item for item in data
        if item['name'] == 'Benner Road'
    ]
    assert len(benner_road_data) == 1
    benner_road_data = benner_road_data[0]
    assert benner_road_data['value'] == (
            Decimal("45.15") * Decimal("5.7")
    )


def test_success__query_all_data__metric_bin__group_by_orchard(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'orchard'
    service = GenerateDashboardServiceV1(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    # action
    data = service.generate()

    # assert
    assert len(data) == 2

    # assert cypress data
    cypress_data = [
        item for item in data
        if item['name'] == 'Cypress'
    ]
    assert len(cypress_data) == 1
    cypress_data = cypress_data[0]
    assert cypress_data['value'] == 36

    # assert benner road data
    benner_road_data = [
        item for item in data
        if item['name'] == 'Benner Road'
    ]
    assert len(benner_road_data) == 1
    benner_road_data = benner_road_data[0]
    assert benner_road_data['value'] == 11
