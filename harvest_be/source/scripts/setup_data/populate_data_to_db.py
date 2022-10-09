# -*- coding: utf-8 -*-
import json
import os
import sys

import django
from django.db import transaction


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
django.setup()
from harvest.models import Harvest
from harvest.models import Orchard
from harvest.models import Variety
from user.models import User


def _create_harvest(row_item):
    """
    row_item = {
        "id": "85fcb37c-74d3-42cb-a3da-e425755e50bd",
        "userId": "5e035584-218f-41ad-bb99-5d2e3c8d7215",
        "orchardId": "-MThSwo4wzyvSPUGdM6h",
        "varietyId": "-M2StWPdhrsVWZjWluBD",
        "hoursWorked": 7.9,
        "orchardName": "Cypress",
        "pickingDate": "2021-05-04T00:04:57.969Z",
        "varietyName": "Pink Lady",
        "numberOfBins": 16,
        "payRatePerHour": 42.36
      }
    """
    print(f"Initializing harvest id {row_item['id']}")
    user, _ = User.objects.get_or_create(
        id=row_item['userId'],
        username={
            'username': row_item['userId']
        }
    )
    orchard, _ = Orchard.objects.get_or_create(
        id=row_item['orchardId'],
        defaults={
            'name': row_item['orchardName']
        }
    )
    variety, _ = Variety.objects.get_or_create(
        id=row_item['varietyId'],
        defaults={
            'name': row_item['varietyName']
        }
    )

    _, created = Harvest.objects.get_or_create(
        id=row_item['id'],
        defaults=dict(
            user=user,
            orchard=orchard,
            variety=variety,
            hours_worked=row_item['hoursWorked'],
            picking_time=row_item['pickingDate'],
            number_of_bins=row_item['numberOfBins'],
            pay_rate_per_hour=row_item['payRatePerHour']
        )
    )

    if created:
        print(f"Done creating harvest id {row_item['id']}")
    else:
        print(f"Harvest id {row_item['id']} existed, ignored!")


@transaction.atomic
def populate_data():
    # read data from file
    file_path = os.path.join(BASE_DIR, 'scripts/setup_data/data.json')
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        for idx, row_item in enumerate(json_data):
            print(idx + 1)
            _create_harvest(row_item)


if __name__ == '__main__':
    populate_data()
