# Generated by Django 3.2.13 on 2022-10-25 12:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0033_workshop'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='workshop_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
