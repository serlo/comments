# Generated by Django 2.2.7 on 2019-11-12 13:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [
        ("threads", "0001_initial"),
        ("threads", "0002_auto_20191022_1129"),
        ("threads", "0003_auto_20191022_1213"),
        ("threads", "0004_auto_20191112_0947"),
        ("threads", "0005_auto_20191112_1305"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=200)),
                ("provider_id", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Entity",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("entity_id", models.CharField(max_length=200)),
                ("provider_id", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Thread",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "entity",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="threads.Entity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField()),
                ("content", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="threads.Author"
                    ),
                ),
                (
                    "thread",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="threads.Thread"
                    ),
                ),
            ],
        ),
    ]
