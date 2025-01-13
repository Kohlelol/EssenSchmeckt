# Generated by Django 5.1.4 on 2025-01-11 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_auto_20250104_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='pdfs/')),
                ('expire_date', models.DateField()),
                ('from_date', models.DateField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
