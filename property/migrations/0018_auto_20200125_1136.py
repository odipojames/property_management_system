# Generated by Django 2.2.6 on 2020-01-25 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0017_auto_20200125_1000'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rent',
            unique_together={('unit', 'year', 'month')},
        ),
    ]
