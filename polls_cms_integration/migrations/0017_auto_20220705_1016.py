# Generated by Django 3.2.13 on 2022-07-05 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0016_auto_20220629_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='langpoll',
            name='care',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='langpoll',
            name='economy',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='langpoll',
            name='embedding',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='langpoll',
            name='ethics',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='langpoll',
            name='law',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='langpoll',
            name='technology',
            field=models.CharField(max_length=400),
        ),
    ]