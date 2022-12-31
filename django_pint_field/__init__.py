"""
Enables pint for use with Django
"""
from django.db import connection
from psycopg2.extras import register_composite
from psycopg2.extensions import adapt, AsIs


__version__ = "0.0.1"

# e.g.: x, y = IntegerPintDBField(magnitude=1, unit="xyz")


def get_IntegerPintDBField():
    return register_composite("integer_pint_field", connection.cursor().cursor, globally=True).type


def get_BigIntegerPintDBField():
    return register_composite("big_integer_pint_field", connection.cursor().cursor, globally=True).type


def get_DecimalPintDBField():
    return register_composite("decimal_pint_field", connection.cursor().cursor, globally=True).type


def integer_pint_field_adapter(value):
    return AsIs(
        "(%s::integer, %s::text)::integer_pint_field"
        % (
            adapt(value.magnitude).getquoted(),
            adapt(str(value.units)).getquoted(),
        )
    )


def big_integer_pint_field_adapter(value):
    return AsIs(
        "(%s::bigint, %s::text)::big_integer_pint_field"
        % (
            adapt(value.magnitude).getquoted(),
            adapt(str(value.units)).getquoted(),
        )
    )


def decimal_pint_field_adapter(value):
    return AsIs(
        "(%s::decimal, %s::text)::decimal_pint_field"
        % (
            adapt(value.magnitude).getquoted(),
            adapt(str(value.units)).getquoted(),
        )
    )
