# Generated by Django 3.0.3 on 2020-03-26 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_app_public_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='secret_key',
            field=models.CharField(max_length=34),
        ),
    ]
