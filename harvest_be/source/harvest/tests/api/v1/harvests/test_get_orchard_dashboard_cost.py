# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest

from harvest.tests.factories.harvest import HarvestFactory
from harvest.tests.factories.orchard import OrchardFactory
from harvest.tests.factories.variety import VarietyFactory
from user.tests.factories.user import UserFactory

pytestmark = pytest.mark.django_db


GROUP_BY = 'orchard'
METRIC = 'cost'


@pytest.fixture
def harvest_data():
    """
    Pick 5 first harvest from json file
    """
    # harvest 1
    user = UserFactory(id='5e035584-218f-41ad-bb99-5d2e3c8d7215')
    orchard = OrchardFactory(
        id='-MThSwo4wzyvSPUGdM6h',
        name='Cypress',
    )
    variety = VarietyFactory(
        id='-M2StWPdhrsVWZjWluBD',
        name='Pink Lady'
    )
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('7.9'),
        picking_time='2021-05-04T00:04:57.969Z',
        number_of_bins=16,
        pay_rate_per_hour=Decimal('42.36')
    )

    # harvest 2
    user = UserFactory(id='334a3eb7-d7bd-40cc-ac5e-801a96703453')
    orchard = OrchardFactory(
        id='-MThSwo4wzyvSPUGdM6h',
        name='Cypress',
    )
    variety = VarietyFactory(
        id='-M2StWPW7APCf0Jn3ew0',
        name='Galaxy'
    )
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('6.1'),
        picking_time='2021-05-09T17:52:23.456Z',
        number_of_bins=13,
        pay_rate_per_hour=Decimal('70.09')
    )

    # harvest 3
    user = UserFactory(id='e153ce3f-127e-446b-a328-0ebea2c706d8')
    orchard = OrchardFactory(
        id='-MThSwo4wzyvSPUGdM6h',
        name='Cypress',
    )
    variety = VarietyFactory(
        id='-M2StWPW7APCf0Jn3ew0',
        name='Galaxy'
    )
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('1.4'),
        picking_time='2021-05-25T17:09:35.387Z',
        number_of_bins=3,
        pay_rate_per_hour=Decimal('76.63')
    )

    # harvest 4
    user = UserFactory(id='e3e22388-fd57-42ed-ac8d-7cdf70d04ed1')
    orchard = OrchardFactory(
        id='-MThT6k5FHYORAhs0klw',
        name='Benner Road',
    )
    variety = VarietyFactory(
        id='-M2StWPil_OVo67-CUm-',
        name='Royal Gala'
    )
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('5.7'),
        picking_time='2021-06-20T10:39:51.999Z',
        number_of_bins=11,
        pay_rate_per_hour=Decimal('45.15')
    )

    # harvest 5
    user = UserFactory(id='81ef66d4-80e6-46f9-bf1b-d40408b0ed52')
    orchard = OrchardFactory(
        id='-MThSwo4wzyvSPUGdM6h',
        name='Cypress',
    )
    variety = VarietyFactory(
        id='-M2StWPW7APCf0Jn3ew0',
        name='Galaxy'
    )
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('6.4'),
        picking_time='2021-06-09T02:13:05.764Z',
        number_of_bins=4,
        pay_rate_per_hour=Decimal('42.67')
    )


def test_success__date_range_has_no_data__time_too_early(
        harvest_data,
        api_client
):
    # arrange params
    start = '2021-02-02T00:00:00Z'
    end = '2021-02-03T00:00:00Z'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        GROUP_BY,
        orchard_ids,
        start,
        end,
        METRIC
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    print(data)
    assert res.status_code == 200
    assert data == []


def test_success__date_range_has_no_data__time_too_far(
        harvest_data,
        api_client
):
    # arrange params
    start = '2023-02-02T00:00:00Z'
    end = '2023-05-30T00:00:00Z'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        GROUP_BY,
        orchard_ids,
        start,
        end,
        METRIC
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    assert res.status_code == 200
    assert data == []


def test_success__date_range_has_partial_data(
        harvest_data,
        api_client
):
    # arrange params
    start = '2021-05-01T00:00:00Z'
    end = '2021-05-30T00:00:00Z'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        GROUP_BY,
        orchard_ids,
        start,
        end,
        METRIC
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    assert res.status_code == 200
    assert len(data) == 1

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
            Decimal("76.63") * Decimal("1.4")
    )


def test_success__date_range_has_full_data(
        harvest_data,
        api_client
):
    # arrange params
    start = '2021-05-01T00:00:00Z'
    end = '2021-06-30T00:00:00Z'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        GROUP_BY,
        orchard_ids,
        start,
        end,
        METRIC
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    assert res.status_code == 200
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


def test_success__date_range_has_full_data__filtered_orchard_has_no_data(
        harvest_data,
        api_client
):
    # arrange params
    start = '2021-05-01T00:00:00Z'
    end = '2021-06-30T00:00:00Z'
    orchard_ids = 'M2StWPXh61bNCQDqglzzzzzzz'

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        GROUP_BY,
        orchard_ids,
        start,
        end,
        METRIC
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    assert res.status_code == 200
    assert len(data) == 0
