# -*- coding: utf-8 -*-

from common.repositories.base import BaseRepository
from harvest.models import Orchard


class OrchardRepository(BaseRepository):
    model = Orchard
