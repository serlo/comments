# Generated by Django 2.2.9 on 2020-01-23 19:29

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("threads", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment", old_name="author", new_name="user",
        ),
        migrations.RenameModel(old_name="Author", new_name="User",),
    ]