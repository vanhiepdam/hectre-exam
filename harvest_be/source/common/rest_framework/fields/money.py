from django.utils.translation import ugettext_lazy as _
from rest_framework.fields import DecimalField


class MoneyField(DecimalField):
    default_error_messages = {
        'invalid': _('The Money Number is invalid.')
    }
    DEFAULT_MIN_VALUE = 0.1
    DEFAULT_MAX_DIGITS = 20
    DEFAULT_MAX_DECIMAL_PLACES = 6

    def __init__(self, **kwargs):
        if 'min_value' not in kwargs:
            kwargs['min_value'] = self.DEFAULT_MIN_VALUE
        if 'max_digits' not in kwargs:
            kwargs['max_digits'] = self.DEFAULT_MAX_DIGITS
        if 'decimal_places' not in kwargs:
            kwargs['decimal_places'] = self.DEFAULT_MAX_DECIMAL_PLACES
        super(MoneyField, self).__init__(**kwargs)
