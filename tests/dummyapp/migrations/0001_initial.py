# Generated by Django 3.2.9 on 2022-04-24 09:40

from django.db import migrations, models

import django_pint_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BigIntFieldSaveModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.BigIntegerPintField(
                        default_unit="gram", unit_choices=["gram"]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ChoicesDefinedInModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    django_pint_field.fields.PintField(
                        default_unit="kilogram", unit_choices=["milligram", "pounds"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChoicesDefinedInModelInt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weight",
                    django_pint_field.fields.IntegerPintField(
                        default_unit="kilogram", unit_choices=["milligram", "pounds"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomUregDecimalHayBale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "custom_decimal",
                    django_pint_field.fields.DecimalPintField(
                        default_unit="custom",
                        decimal_places=2,
                        max_digits=10,
                        unit_choices=["custom"],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CustomUregHayBale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "custom",
                    django_pint_field.fields.PintField(
                        default_unit="custom", unit_choices=["custom"]
                    ),
                ),
                (
                    "custom_int",
                    django_pint_field.fields.IntegerPintField(
                        default_unit="custom", unit_choices=["custom"]
                    ),
                ),
                (
                    "custom_bigint",
                    django_pint_field.fields.BigIntegerPintField(
                        default_unit="custom", unit_choices=["custom"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DecimalFieldSaveModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.DecimalPintField(
                        default_unit="gram",
                        decimal_places=2,
                        max_digits=10,
                        unit_choices=["gram"],
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EmptyHayBaleBigInt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.BigIntegerPintField(
                        default_unit="gram", null=True, unit_choices=["gram"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmptyHayBaleDecimal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.DecimalPintField(
                        default_unit="gram",
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        unit_choices=["gram"],
                    ),
                ),
                (
                    "compare",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmptyHayBaleFloat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.PintField(
                        default_unit="gram", null=True, unit_choices=["gram"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmptyHayBaleInt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.IntegerPintField(
                        default_unit="gram", null=True, unit_choices=["gram"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmptyHayBalePositiveInt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.PositiveIntegerPintField(
                        default_unit="gram", null=True, unit_choices=["gram"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FloatFieldSaveModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.PintField(
                        default_unit="gram", unit_choices=["gram"]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="HayBale",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.PintField(
                        default_unit="gram", unit_choices=["gram"]
                    ),
                ),
                (
                    "weight_int",
                    django_pint_field.fields.IntegerPintField(
                        default_unit="gram", blank=True, null=True, unit_choices=["gram"]
                    ),
                ),
                (
                    "weight_bigint",
                    django_pint_field.fields.BigIntegerPintField(
                        default_unit="gram", blank=True, null=True, unit_choices=["gram"]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="IntFieldSaveModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                (
                    "weight",
                    django_pint_field.fields.IntegerPintField(
                        default_unit="gram", unit_choices=["gram"]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
