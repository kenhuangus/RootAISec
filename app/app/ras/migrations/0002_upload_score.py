# Generated by Django 5.0.6 on 2024-05-30 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='score',
            field=models.FloatField(default=0.0),
        ),
    ]