import pytest

import django.core.exceptions
import django.core.validators
from django.core.serializers import deserialize, serialize
from django.db import transaction
from django.db.models import Field, Model
from django.test import TestCase

import json
import warnings
from decimal import Decimal
from pint import DimensionalityError, UndefinedUnitError, UnitRegistry
from typing import Type, Union

from django_pint_field.fields import (
    BigIntegerPintField,
    DecimalPintField,
    IntegerPintField,
)
from django_pint_field.units import ureg
from tests.dummyapp.models import (
    BigIntegerPintFieldSaveModel,
    ChoicesDefinedInModel,
    CustomUregHayBale,
    EmptyHayBaleBigInteger,
    EmptyHayBaleDecimal,
    EmptyHayBaleInteger,
    HayBale,
    FieldSaveModel,
    IntegerPintFieldSaveModel,
    DecimalPintFieldSaveModel,
)

Quantity = ureg.Quantity


class BaseMixinTestFieldCreate:
    # The field that needs to be tested
    FIELD: Type[Field]
    # Some fields, i.e. the decimal require default kwargs to work properly
    DEFAULT_KWARGS = {}

    # def test_sets_units(self):
    #     test_grams = self.FIELD("gram", **self.DEFAULT_KWARGS)
    #     self.assertEqual(test_grams.units, ureg.gram)

    def test_fails_with_unknown_units(self):
        with self.assertRaises(UndefinedUnitError):
            test_crazy_units = self.FIELD("zinghie", **self.DEFAULT_KWARGS)  # noqa: F841

    def test_default_unit_is_required(self):
        with self.assertRaises(TypeError):
            no_units = self.FIELD(**self.DEFAULT_KWARGS)  # noqa: F841

    def test_default_unit_set_with_name(self):
        okay_units = self.FIELD(default_unit="meter", **self.DEFAULT_KWARGS)  # noqa: F841

    def test_default_unit_are_invalid(self):
        with self.assertRaises(ValueError):
            wrong_units = self.FIELD(None, **self.DEFAULT_KWARGS)  # noqa: F841

    def test_unit_choices_must_be_valid_units(self):
        with self.assertRaises(UndefinedUnitError):
            self.FIELD(default_unit="mile", unit_choices=["gunzu"], **self.DEFAULT_KWARGS)

    def test_unit_choices_must_match_base_dimensionality(self):
        with self.assertRaises(DimensionalityError):
            self.FIELD(default_unit="gram", unit_choices=["meter", "ounces"], **self.DEFAULT_KWARGS)


class TestIntegerFieldCreate(BaseMixinTestFieldCreate, TestCase):
    FIELD = IntegerPintField


class TestBigIntegerFieldCreate(BaseMixinTestFieldCreate, TestCase):
    FIELD = BigIntegerPintField


class TestDecimalFieldCreate(BaseMixinTestFieldCreate, TestCase):
    FIELD = DecimalPintField
    DEFAULT_KWARGS = {"max_digits": 10, "decimal_places": 2}


@pytest.mark.parametrize(
    "max_digits, decimal_places, error",
    [
        (None, None, "Invalid initialization.*expect.*integers.*"),
        (10, None, "Invalid initialization.*expect.*integers.*"),
        (None, 2, "Invalid initialization.*expect.*integers.*"),
        (-1, 2, "Invalid initialization.*positive.*larger than decimal_places.*"),
        (2, -1, "Invalid initialization.*positive.*larger than decimal_places.*"),
        (2, 3, "Invalid initialization.*positive.*larger than decimal_places.*"),
    ],
)
def test_decimal_init_fail(max_digits, decimal_places, error):
    with pytest.raises(ValueError, match=error):
        DecimalPintField("meter", max_digits=max_digits, decimal_places=decimal_places)


@pytest.mark.parametrize("max_digits, decimal_places", [(2, 0), (2, 2), (1, 0)])
def decimal_init_success(max_digits, decimal_places):
    DecimalPintField("meter", max_digits=max_digits, decimal_places=decimal_places)


@pytest.mark.django_db
class TestCustomUreg(TestCase):
    def setUp(self):
        # Custom Values are fined in confest.py
        CustomUregHayBale.objects.create(
            custom_int=5 * ureg.custom,
            custom_bigint=5 * ureg.custom,
            custom_decimal=Decimal("5") * ureg.custom,
        )
        CustomUregHayBale.objects.create(
            custom_int=5 * ureg.kilocustom,
            custom_bigint=5 * ureg.kilocustom,
            custom_decimal=Decimal("5") * ureg.kilocustom,
        )

    def tearDown(self):
        CustomUregHayBale.objects.all().delete()

    def test_custom_ureg_int(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom_int, ureg.Quantity)
        self.assertEqual(str(obj.custom_int), "5 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom_int.to_root_units()), "5000 custom")

    def test_custom_ureg_bigint(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom_bigint, ureg.Quantity)
        self.assertEqual(str(obj.custom_bigint), "5 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom_bigint.to_root_units()), "5000 custom")

    def test_custom_ureg_decimal(self):
        obj = CustomUregHayBale.objects.first()
        self.assertIsInstance(obj.custom_decimal, ureg.Quantity)
        self.assertEqual(str(obj.custom_decimal), "5.00 custom")

        obj = CustomUregHayBale.objects.last()
        self.assertEqual(str(obj.custom_decimal.to_root_units()), "5000.00 custom")


class BaseMixinNullAble:
    EMPTY_MODEL: Type[Model]
    FLOAT_SET_STR = "707.7"
    FLOAT_SET = Decimal(FLOAT_SET_STR)  # ToDo: NEED WORK HERE
    DB_FLOAT_VALUE_EXPECTED = 707.7

    def setUp(self):
        self.EMPTY_MODEL.objects.create(name="Empty")

    def tearDown(self) -> None:
        self.EMPTY_MODEL.objects.all().delete()

    def test_accepts_assigned_null(self):
        new = self.EMPTY_MODEL()
        new.weight = None
        new.name = "Test"
        new.save()
        self.assertIsNone(new.weight)
        # Also get it from database to verify
        from_db = self.EMPTY_MODEL.objects.last()
        self.assertIsNone(from_db.weight)

    def test_accepts_auto_null(self):
        empty = self.EMPTY_MODEL.objects.first()
        self.assertIsNone(empty.weight, None)

    def test_accepts_default_pint_unit(self):
        new = self.EMPTY_MODEL(name="DefaultPintUnitTest")
        units = UnitRegistry()
        new.weight = 5 * units.kilogram
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "DefaultPintUnitTest")
        self.assertEqual(str(obj.weight.to_root_units().units), "gram")
        self.assertEqual(obj.weight.to_root_units().magnitude, 5000)

    def test_accepts_default_app_unit(self):
        new = self.EMPTY_MODEL(name="DefaultAppUnitTest")
        new.weight = 5 * ureg.kilogram
        # Make sure that the correct argument does not raise a warning
        with warnings.catch_warnings(record=True) as w:
            new.save()
        assert len(w) == 0
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "DefaultAppUnitTest")
        self.assertEqual(obj.weight.to_root_units().units, "gram")
        self.assertEqual(obj.weight.to_root_units().magnitude, 5000)

    def test_accepts_assigned_whole_number_quantity(self):
        new = self.EMPTY_MODEL(name="WholeNumber")
        new.weight = Quantity(707 * ureg.gram)
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "WholeNumber")
        self.assertEqual(obj.weight.units, "gram")
        self.assertEqual(obj.weight.magnitude, 707)

    def test_accepts_assigned_float_number_quantity(self):
        new = self.EMPTY_MODEL(name="FloatNumber")
        new.weight = Quantity(self.FLOAT_SET * ureg.gram)
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "FloatNumber")
        self.assertEqual(obj.weight.units, "gram")
        # We expect the database to deliver the correct type, at least
        # for postgresql this is true
        self.assertEqual(obj.weight.magnitude, self.DB_FLOAT_VALUE_EXPECTED)
        self.assertIsInstance(obj.weight.magnitude, type(self.DB_FLOAT_VALUE_EXPECTED))

    def test_serialisation(self):
        serialized = serialize(
            "json",
            [
                self.EMPTY_MODEL.objects.first(),
            ],
        )
        deserialized = json.loads(serialized)
        obj = deserialized[0]["fields"]
        self.assertEqual(obj["name"], "Empty")
        self.assertIsNone(obj["weight"])
        obj_generator = deserialize("json", serialized, ignorenonexistent=True)
        obj_back = next(obj_generator)
        self.assertEqual(obj_back.object.name, "Empty")
        self.assertIsNone(obj_back.object.weight)


@pytest.mark.django_db
class TestNullableInteger(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleInteger
    DB_FLOAT_VALUE_EXPECTED = int(BaseMixinNullAble.FLOAT_SET)


@pytest.mark.django_db
class TestNullableBigInteger(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleBigInteger
    DB_FLOAT_VALUE_EXPECTED = int(BaseMixinNullAble.FLOAT_SET)


@pytest.mark.django_db
class TestNullableDecimal(BaseMixinNullAble, TestCase):
    EMPTY_MODEL = EmptyHayBaleDecimal
    DB_FLOAT_VALUE_EXPECTED = Decimal(BaseMixinNullAble.FLOAT_SET_STR)

    def test_with_default_implementation(self):
        new = self.EMPTY_MODEL(name="FloatNumber")
        new.weight = Quantity(self.FLOAT_SET * ureg.gram)
        new.compare = self.FLOAT_SET
        new.save()
        obj = self.EMPTY_MODEL.objects.last()
        self.assertEqual(obj.name, "FloatNumber")
        self.assertEqual(obj.weight.units, "gram")
        # We compare with the reference implementation of django, this should
        # be always true no matter which database is used
        self.assertEqual(obj.weight.magnitude, obj.compare)
        self.assertIsInstance(obj.weight.magnitude, type(obj.compare))
        # We also expect (at least for postgresql) that this a Decimal
        self.assertEqual(obj.weight.magnitude, self.DB_FLOAT_VALUE_EXPECTED)
        self.assertIsInstance(obj.weight.magnitude, Decimal)


class FieldSaveTestBase:
    MODEL: Type[FieldSaveModel]
    EXPECTED_TYPE: Type = float
    DEFAULT_WEIGHT = 100
    DEFAULT_WEIGHT_STR = "100.0"
    DEFAULT_WEIGHT_QUANTITY_STR = "100.0 gram"
    HEAVIEST = 1000
    LIGHTEST = 1
    OUNCE_VALUE = 3.52739619496
    COMPARE_QUANTITY = Quantity(0.8 * ureg.ounce)  # 1 ounce = 28.34 grams

    def setUp(self):
        if self.EXPECTED_TYPE == Decimal:
            self.MODEL.objects.create(
                weight=Quantity(Decimal(str(self.DEFAULT_WEIGHT)) * ureg.gram),
                name="grams",
            )
            self.lightest = self.MODEL.objects.create(
                weight=Quantity(Decimal(str(self.LIGHTEST)) * ureg.gram),
                name="lightest",
            )
            self.heaviest = self.MODEL.objects.create(
                weight=Quantity(Decimal(str(self.HEAVIEST)) * ureg.gram),
                name="heaviest",
            )
        else:
            self.MODEL.objects.create(
                weight=Quantity(self.DEFAULT_WEIGHT * ureg.gram),
                name="grams",
            )
            self.lightest = self.MODEL.objects.create(
                weight=Quantity(self.LIGHTEST * ureg.gram),
                name="lightest",
            )
            self.heaviest = self.MODEL.objects.create(
                weight=Quantity(self.HEAVIEST * ureg.gram),
                name="heaviest",
            )

    def tearDown(self):
        self.MODEL.objects.all().delete()

    # def test_fails_with_incompatible_units(self):
    #     # we have to wrap this in a transaction
    #     # fixing a unit test problem
    #     # http://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
    #     metres = Quantity(100 * ureg.meter)
    #     with transaction.atomic():
    #         with self.assertRaises(DimensionalityError):
    #             self.MODEL.objects.create(weight=metres, name="Should Fail")

    def test_value_stored_as_quantity(self):
        obj = self.MODEL.objects.first()
        self.assertIsInstance(obj.weight, Quantity)
        self.assertEqual(str(obj.weight), self.DEFAULT_WEIGHT_QUANTITY_STR)

    def test_value_stored_as_correct_magnitude_type(self):
        obj = self.MODEL.objects.first()
        self.assertIsInstance(obj.weight, Quantity)
        self.assertIsInstance(obj.weight.magnitude, self.EXPECTED_TYPE)

    def test_value_conversion(self):
        obj = self.MODEL.objects.first()
        ounces = obj.weight.to(ureg.ounce)
        self.assertAlmostEqual(ounces.magnitude, self.OUNCE_VALUE)
        self.assertEqual(ounces.units, ureg.ounce)

    def test_order_by(self):
        qs = list(self.MODEL.objects.all().order_by("weight"))
        self.assertEqual(qs[0].name, "lightest")
        self.assertEqual(qs[-1].name, "heaviest")
        self.assertEqual(qs[0], self.lightest)
        self.assertEqual(qs[-1], self.heaviest)

    # The two following functions cause this error:
    #   psycopg2.errors.DatatypeMismatch: cannot compare dissimilar column types bigint and integer at record column 1
    #   django.db.utils.ProgrammingError: cannot compare dissimilar column types bigint and integer at record column 1

    # def test_comparison_with_quantity(self):
    #     weight = Quantity(2 * ureg.gram)
    #     qs = self.MODEL.objects.filter(weight__gt=weight)
    #     self.assertNotIn(self.lightest, qs)

    # def test_comparison_with_quantity_respects_units(self):
    #     qs = self.MODEL.objects.filter(weight__gt=self.COMPARE_QUANTITY)
    #     self.assertNotIn(self.lightest, qs)

    def test_serialisation(self):
        serialized = serialize(
            "json",
            [
                self.MODEL.objects.first(),
            ],
        )
        deserialized = json.loads(serialized)
        obj = deserialized[0]["fields"]
        self.assertEqual(obj["weight"], self.DEFAULT_WEIGHT_QUANTITY_STR)


class TestDecimalFieldSave(FieldSaveTestBase, TestCase):
    MODEL = DecimalPintFieldSaveModel
    DEFAULT_WEIGHT_QUANTITY_STR = "100.00 gram"
    OUNCES = Decimal("10") * ureg.ounce
    OUNCE_VALUE = Decimal("3.52739619496")
    OUNCES_IN_GRAM = Decimal("283.50")
    EXPECTED_TYPE = Decimal


class IntLikeFieldSaveTestBase(FieldSaveTestBase):
    DEFAULT_WEIGHT_QUANTITY_STR = "100 gram"
    EXPECTED_TYPE = int
    # 1 ounce = 28.34 grams -> we use something that can be stored as int
    COMPARE_QUANTITY = Quantity(Decimal(str(28 * 1000)) * ureg.milligram)


class TestIntFieldSave(IntLikeFieldSaveTestBase, TestCase):
    MODEL = IntegerPintFieldSaveModel


class TestBigIntFieldSave(IntLikeFieldSaveTestBase, TestCase):
    MODEL = BigIntegerPintFieldSaveModel