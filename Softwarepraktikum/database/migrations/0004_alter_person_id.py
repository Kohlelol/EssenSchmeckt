# Generated by Django 3.2.25 on 2024-11-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20241117_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.UUIDField(primary_key=True, serialize=False),
        ),
    ]
