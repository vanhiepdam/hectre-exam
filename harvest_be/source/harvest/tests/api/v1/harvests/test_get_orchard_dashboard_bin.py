# -*- coding: utf-8 -*-

import pytest

pytestmark = pytest.mark.django_db

GROUP_BY = 'orchard'
METRIC = 'bin'


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
    assert cypress_data['value'] == 32


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
    assert cypress_data['value'] == 36

    # assert benner road data
    benner_road_data = [
        item for item in data
        if item['name'] == 'Benner Road'
    ]
    assert len(benner_road_data) == 1
    benner_road_data = benner_road_data[0]
    assert benner_road_data['value'] == 11


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


def test_failure__group_by_not_valid(
        harvest_data,
        api_client
):
    # arrange params
    start = '2021-05-01T00:00:00Z'
    end = '2021-06-30T00:00:00Z'
    orchard_ids = ''

    # arrange payload
    url = '/api/v1/harvests/dashboard/?group_by={}&orchard_ids={}&start_time={}&end_time={}&metric={}'.format(
        'binn',
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
    assert res.status_code == 400
    assert data['messages'][0] == '"binn" is not a valid choice.'


def test_failure__metric_not_valid(
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
        'variety'
    )

    # action
    res = api_client.get(
        url,
        content_type='application/json',
    )
    data = res.data

    # assert
    assert res.status_code == 400
    assert data['messages'][0] == '"variety" is not a valid choice.'
