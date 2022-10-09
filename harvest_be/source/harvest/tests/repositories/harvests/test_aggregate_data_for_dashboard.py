# -*- coding: utf-8 -*-
from datetime import datetime

import pytest

from harvest.repositories.harvest import HarvestRepository
from harvest.repositories.orchard import OrchardRepository

pytestmark = pytest.mark.django_db


def test_success__aggregate_full_data__orchards_are_none(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'variety'

    # action
    data = HarvestRepository.aggregate_data_for_dashboard(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by
    )

    #  assert
    data = list(data)
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


def test_success__aggregate_full_data__orchards_are_fulfilled(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'variety'

    # arrange orchard
    orchard = OrchardRepository.get_by_id(
        '-MThT6k5FHYORAhs0klw'
    )

    # action
    data = HarvestRepository.aggregate_data_for_dashboard(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by,
        orchards=[orchard]
    )

    #  assert
    data = list(data)
    assert len(data) == 1
    # assert royal gala data
    royal_gala_data = [
        item for item in data
        if item['name'] == 'Royal Gala'
    ]
    assert len(royal_gala_data) == 1
    royal_gala_data = royal_gala_data[0]
    assert royal_gala_data['value'] == 11


def test_success__aggregate_full_data__orchards_are_empty(harvest_data):
    # arrange
    start_time = datetime(year=2020, month=1, day=1)
    end_time = datetime(year=2023, month=1, day=1)
    metric = 'bin'
    group_by = 'variety'

    # action
    data = HarvestRepository.aggregate_data_for_dashboard(
        start_time=start_time,
        end_time=end_time,
        metric=metric,
        group_by=group_by,
        orchards=[]
    )

    #  assert
    data = list(data)
    assert len(data) == 0
