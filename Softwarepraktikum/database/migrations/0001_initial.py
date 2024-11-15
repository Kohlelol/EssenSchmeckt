# Generated by Django 3.2.25 on 2024-11-15 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField()),
                ('qr_code', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
    ]
