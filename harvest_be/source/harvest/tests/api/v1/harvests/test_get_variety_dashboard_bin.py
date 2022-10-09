# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest

from harvest.tests.factories.harvest import HarvestFactory
from harvest.tests.factories.orchard import OrchardFactory
from harvest.tests.factories.variety import VarietyFactory
from user.tests.factories.user import UserFactory


GROUP_BY = 'variety'
METRIC = 'bin'


@pytest.fixture
def harvest_data():
    """
    Pick 5 first harvest from json file
    """
    # harvest 1
    user = UserFactory(id='5e035584-218f-41ad-bb99-5d2e3c8d7215')
    orchard = OrchardFactory(id='-MThSwo4wzyvSPUGdM6h')
    variety = VarietyFactory(id='-M2StWPdhrsVWZjWluBD')
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('7.9'),
        picking_date='2021-05-04T00:04:57.969Z',
        number_of_bins=16,
        pay_rate_per_hour=Decimal('42.36')
    )

    # harvest 2
    user = UserFactory(id='334a3eb7-d7bd-40cc-ac5e-801a96703453')
    orchard = OrchardFactory(id='-MThSwo4wzyvSPUGdM6h')
    variety = VarietyFactory(id='-M2StWPW7APCf0Jn3ew0')
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('6.1'),
        picking_date='2021-05-09T17:52:23.456Z',
        number_of_bins=13,
        pay_rate_per_hour=Decimal('70.09')
    )

    # harvest 3
    user = UserFactory(id='e153ce3f-127e-446b-a328-0ebea2c706d8')
    orchard = OrchardFactory(id='-MThSwo4wzyvSPUGdM6h')
    variety = VarietyFactory(id='-M2StWPW7APCf0Jn3ew0')
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('1.4'),
        picking_date='2021-05-25T17:09:35.387Z',
        number_of_bins=3,
        pay_rate_per_hour=Decimal('76.63')
    )

    # harvest 4
    user = UserFactory(id='e3e22388-fd57-42ed-ac8d-7cdf70d04ed1')
    orchard = OrchardFactory(id='-MThT6k5FHYORAhs0klw')
    variety = VarietyFactory(id='-M2StWPil_OVo67-CUm-')
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('5.7'),
        picking_date='2021-06-20T10:39:51.999Z',
        number_of_bins=11,
        pay_rate_per_hour=Decimal('45.15')
    )

    # harvest 5
    user = UserFactory(id='81ef66d4-80e6-46f9-bf1b-d40408b0ed52')
    orchard = OrchardFactory(id='-MThSwo4wzyvSPUGdM6h')
    variety = VarietyFactory(id='-M2StWPW7APCf0Jn3ew0')
    HarvestFactory(
        user=user,
        orchard=orchard,
        variety=variety,
        hours_worked=Decimal('6.4'),
        picking_date='2021-06-09T02:13:05.764Z',
        number_of_bins=4,
        pay_rate_per_hour=Decimal('42.67')
    )


def test_success__date_range_has_no_data__time_too_early(
        harvest_data,
        api_client
):
    # arrange params
    start = '02/02/2021'
    end = '03/02/2021'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start={}&end={}&metric={}'.format(
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


def test_success__date_range_has_no_data__time_too_far(
        harvest_data,
        api_client
):
    # arrange params
    start = '02/02/2023'
    end = '03/02/2023'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start={}&end={}&metric={}'.format(
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
    start = '01/05/2021'
    end = '30/05/2021'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start={}&end={}&metric={}'.format(
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
    assert galaxy_data['value'] == 16


def test_success__date_range_has_full_data(
        harvest_data,
        api_client
):
    # arrange params
    start = '01/05/2021'
    end = '30/06/2021'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start={}&end={}&metric={}'.format(
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


def test_success__date_range_has_full_data__filtered_orchard_has_no_data(
        harvest_data,
        api_client
):
    # arrange params
    start = '01/05/2021'
    end = '30/06/2021'
    orchard_ids = '-M2StWPXh61bNCQDqglz'

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start={}&end={}&metric={}'.format(
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
