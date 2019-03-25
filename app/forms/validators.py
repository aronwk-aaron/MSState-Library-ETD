import phonenumbers
import pycountry
from wtforms import ValidationError


# noinspection PyBroadException,PyUnusedLocal
def validate_phone(form, field):
    """Validates a field for a valid phone number

    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data

    Returns:
        None, raises ValidationError if failed
    """
    if len(field.data) > 16:
        raise ValidationError('Invalid phone number')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')
    except Exception:
        input_number = phonenumbers.parse('+1' + field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')


# noinspection PyBroadException,PyUnusedLocal
def validate_subdivision(form, field):
    """Validates a field for a valid phone number

    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data

    Returns:
        None, raises ValidationError if failed
    """
    #  TODO: check to see if subdivision is in selected country
    try:
        pycountry.subdivisions.lookup(field.data)
    except Exception:
        raise ValidationError(field.data + ' is not a State / Province / Region')
