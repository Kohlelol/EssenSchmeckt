# Generated by Django 3.2.25 on 2024-11-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_alter_group_group_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='facility_id',
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.UUIDField(default=None, editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='food_for_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('food', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Food for day',
                'verbose_name_plural': 'Food per day',
                'unique_together': {('date', 'food')},
            },
        ),
    ]
