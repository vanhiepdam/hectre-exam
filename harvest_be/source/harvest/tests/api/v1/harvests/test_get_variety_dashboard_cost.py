# -*- coding: utf-8 -*-
from decimal import Decimal

import pytest

pytestmark = pytest.mark.django_db

GROUP_BY = 'variety'
METRIC = 'cost'


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
    assert len(data) == 2

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
            Decimal("70.09") * Decimal("6.1")
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
