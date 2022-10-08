from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import CharField

from common.rest_framework.exceptions import DRFValidationError
from common.utilities.web3 import Web3Util


class EVMAddressField(CharField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        if not Web3Util.is_address(data):
            raise DRFValidationError(_("Address {} is not valid.").format(value))
        return value
