# Generated by Django 2.2.6 on 2020-03-07 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0024_auto_20200306_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='type',
            field=models.CharField(choices=[('shop', 'shop'), ('single', 'single'), ('bedsita', 'bedsita'), ('one bedroom', 'one bedroom'), ('two bedroom', 'two bedroom'), ('three bedroom', 'three bedroom'), ('four bedroom', 'four bedroom')], max_length=30, null=True),
        ),
    ]
