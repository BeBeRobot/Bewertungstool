# Generated by Django 3.2.13 on 2022-10-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0032_setting_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=50)),
                ('workshop_id', models.CharField(max_length=50)),
                ('workshop_name', models.CharField(max_length=100)),
            ],
        ),
    ]
