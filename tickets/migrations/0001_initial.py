# Generated by Django 5.2.1 on 2025-05-14 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("flights", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
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
                ("passenger_name", models.CharField(max_length=100)),
                ("row", models.PositiveIntegerField()),
                ("seat", models.CharField(max_length=1)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("booked", "Booked"),
                            ("canceled", "Canceled"),
                            ("checked_in", "Checked In"),
                        ],
                        default="booked",
                        max_length=20,
                    ),
                ),
                (
                    "flight",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="flights.flight",
                    ),
                ),
            ],
            options={
                "unique_together": {("flight", "row", "seat")},
            },
        ),
    ]
