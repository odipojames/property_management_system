# Generated by Django 2.2.6 on 2020-02-26 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0021_auto_20200225_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rent',
            options={'get_latest_by': ('month', 'year'), 'ordering': ('-year', 'month', 'unit')},
        ),
    ]