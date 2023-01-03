"""
Enables pint for use with Django
"""
import logging
from decimal import Decimal
from django.db import connection
from pint import Quantity
from psycopg2.extras import register_composite
from psycopg2.extensions import adapt, AsIs
from decimal import Decimal

from django.db import connection


logger = logging.getLogger("django_pint_field")


with connection.cursor() as curs:
    curs.execute(
        """
        DO $$ BEGIN
            CREATE TYPE integer_pint_field AS (comparator decimal, magnitude integer, units text);
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """
    )
    curs.execute(
        """
        DO $$ BEGIN
            CREATE TYPE big_integer_pint_field as (comparator decimal, magnitude bigint, units text);
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """
    )
    curs.execute(
        """
        DO $$ BEGIN
            CREATE TYPE decimal_pint_field as (comparator decimal, magnitude decimal, units text);
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        """
    )


def get_base_unit_magnitude(value):
    """
    Provided a value (of type=Quantity), returns the magnitude of that quantity, converted to base units

    If the input is a float, we round it before converting.
    """
    if not isinstance(value.magnitude, Decimal) and not isinstance(value.magnitude, int):
        # The magnitude may be input as a float, but we want it as only int (or Decimal). If we allow it to be converted
        #   from a float value, we might record a comparator value with more precision than actually desired.
        int_magnitude = round(value.magnitude)
        value = Quantity(int_magnitude * value.units)

    comparator_value = value.to_base_units()

    return Decimal(str(comparator_value.magnitude))


# e.g.: x, y, z = IntegerPintDBField(comparator=Decimal("1.00"), magnitude=1, units="xyz")
# In [1]: IntegerPintDBField(comparator=Decimal("1.00"), magnitude=1, units="xyz")
# Out[1]: integer_pint_field(comparator=Decimal('1.00'), magnitude=1, units='xyz')

IntegerPintDBField = register_composite("integer_pint_field", connection.cursor().cursor, globally=True).type
BigIntegerPintDBField = register_composite("big_integer_pint_field", connection.cursor().cursor, globally=True).type
DecimalPintDBField = register_composite("decimal_pint_field", connection.cursor().cursor, globally=True).type


def integer_pint_field_adapter(value):
    comparator = adapt(value.comparator)
    magnitude = adapt(value.magnitude)
    units = adapt(str(value.units))
    return AsIs(
        "(%s::decimal, %s::integer, %s::text)"
        % (
            comparator,
            magnitude,
            units,
        )
    )


def big_integer_pint_field_adapter(value):
    comparator = adapt(value.comparator)
    magnitude = adapt(value.magnitude)
    units = adapt(str(value.units))
    return AsIs(
        "(%s::decimal, %s::bigint, %s::text)"
        % (
            comparator,
            magnitude,
            units,
        )
    )


def decimal_pint_field_adapter(value):
    comparator = adapt(value.comparator)
    magnitude = adapt(value.magnitude)
    units = adapt(str(value.units))
    return AsIs(
        "(%s::decimal, %s::decimal, %s::text)"
        % (
            comparator,
            magnitude,
            units,
        )
    )
