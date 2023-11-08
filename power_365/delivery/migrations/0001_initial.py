# Generated by Django 4.2.4 on 2023-11-06 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryRequest",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("title", models.CharField(max_length=200)),
                ("origin", models.CharField(max_length=255)),
                ("destination", models.CharField(max_length=255)),
                ("product_description", models.TextField(blank=True, null=True)),
                ("pickup_code", models.CharField(max_length=32)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("waiting", "waiting"),
                            ("picked up", "picked up"),
                            ("on transit", "on transit"),
                            ("delivered", "delivered"),
                        ],
                        default="waiting",
                        max_length=255,
                    ),
                ),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="agent",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_modified"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Pickup",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("first_name", models.CharField(max_length=32)),
                ("family_name", models.CharField(max_length=32)),
                ("phone", models.CharField(max_length=32)),
                ("email", models.EmailField(max_length=32)),
                (
                    "delivery_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="delivery.deliveryrequest",
                    ),
                ),
            ],
            options={
                "ordering": ["-date_modified"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DeliveryActivity",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                ("date_modified", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("waiting", "waiting"),
                            ("picked up", "picked up"),
                            ("on transit", "on transit"),
                            ("delivered", "delivered"),
                        ],
                        max_length=255,
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                (
                    "delivery_request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="delivery.deliveryrequest",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-date_modified"],
                "abstract": False,
            },
        ),
    ]
