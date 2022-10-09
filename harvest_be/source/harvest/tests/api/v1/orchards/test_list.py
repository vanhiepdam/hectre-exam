# -*- coding: utf-8 -*-
import pytest

from harvest.tests.factories.orchard import OrchardFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def orchards_fixture():
    hectre = OrchardFactory(
        id='hectre',
        name='hectre'
    )
    hiep = OrchardFactory(
        id='hiep',
        name='hiep',
    )
    return [
        hectre,
        hiep
    ]


def test_success__list_all_orchards(orchards_fixture, api_client):
    # arrange
    url = '/api/v1/orchards/'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 2


def test_success__list_all_orchards__search_by_correct_id(orchards_fixture, api_client):
    # arrange
    hectre_orchard = orchards_fixture[0]
    url = f'/api/v1/orchards/?search={hectre_orchard.id}'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 1
    assert res.data['results'][0]['id'] == hectre_orchard.id
    assert res.data['results'][0]['name'] == hectre_orchard.name


def test_success__list_all_orchards__search_by_part_of_id(orchards_fixture, api_client):
    # arrange
    hectre_orchard = orchards_fixture[0]
    url = f'/api/v1/orchards/?search={hectre_orchard.id[:5]}'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 1
    assert res.data['results'][0]['id'] == hectre_orchard.id
    assert res.data['results'][0]['name'] == hectre_orchard.name


def test_success__list_all_orchards__search_by_correct_name(orchards_fixture, api_client):
    # arrange
    hiep_orchard = orchards_fixture[1]
    url = f'/api/v1/orchards/?search={hiep_orchard.name}'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 1
    assert res.data['results'][0]['id'] == hiep_orchard.id
    assert res.data['results'][0]['name'] == hiep_orchard.name


def test_success__list_all_orchards__search_by_part_of_name(orchards_fixture, api_client):
    # arrange
    hiep_orchard = orchards_fixture[1]
    url = f'/api/v1/orchards/?search={hiep_orchard.name[:3]}'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 1
    assert res.data['results'][0]['id'] == hiep_orchard.id
    assert res.data['results'][0]['name'] == hiep_orchard.name


def test_failure__list_all_orchards__search_by_incorrect_id(orchards_fixture, api_client):
    # arrange
    url = '/api/v1/orchards/?search=627128'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 0


def test_failure__list_all_orchards__search_by_incorrect_name(orchards_fixture, api_client):
    # arrange
    url = '/api/v1/orchards/?search=lalaalalala'

    # action
    res = api_client.get(
        url,
        content_type='application/json'
    )

    # assert
    assert res.status_code == 200
    assert len(res.data['results']) == 0
