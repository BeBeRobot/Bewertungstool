# Generated by Django 3.2.13 on 2022-08-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0030_auto_20220802_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='akupoll',
            name='ques_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ambupoll',
            name='ques_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='langpoll',
            name='ques_id',
            field=models.IntegerField(default=0),
        ),
    ]
