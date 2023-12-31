# Generated by Django 3.2.13 on 2022-06-29 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_cms_integration', '0014_choice'),
    ]

    operations = [
        migrations.CreateModel(
            name='LangPoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('economy', models.CharField(max_length=200)),
                ('care', models.CharField(max_length=200)),
                ('technology', models.CharField(max_length=200)),
                ('embedding', models.CharField(max_length=200)),
                ('law', models.CharField(max_length=200)),
                ('ethics', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='choice',
            name='encuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls_cms_integration.langpoll'),
        ),
        migrations.DeleteModel(
            name='Encuesta',
        ),
    ]
