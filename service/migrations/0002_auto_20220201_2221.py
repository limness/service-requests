# Generated by Django 3.2.8 on 2022-02-01 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='car',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='', max_length=128),
        ),
    ]
