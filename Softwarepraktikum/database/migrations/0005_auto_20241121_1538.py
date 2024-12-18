# Generated by Django 3.2.25 on 2024-11-21 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0004_alter_person_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='person', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
