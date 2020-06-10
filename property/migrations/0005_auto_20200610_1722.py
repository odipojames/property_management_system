# Generated by Django 2.2.6 on 2020-06-10 17:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0004_auto_20200427_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damage',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 6, 10, 17, 22, 31, 982226, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=6),
        ),
        migrations.AlterField(
            model_name='rent',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=6),
        ),
    ]