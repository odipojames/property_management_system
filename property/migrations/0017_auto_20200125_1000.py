# Generated by Django 2.2.6 on 2020-01-25 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0016_auto_20200125_0944'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rent',
            unique_together=set(),
        ),
    ]
