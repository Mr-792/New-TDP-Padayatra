# Generated by Django 4.1.4 on 2023-01-23 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Feed', '0003_polls_end_date_polls_start_date_polls_thoughts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
