# Generated by Django 2.2.6 on 2020-04-22 11:46

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.", regex='^(?:\\+)')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Allocated_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='IbgaroMessageCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('total_messages_sent', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=300, unique=True)),
                ('code', models.CharField(max_length=300, unique=True)),
                ('location', models.CharField(max_length=300)),
                ('number_of_units', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('number_of_floors', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=300, null=True)),
                ('ID_or_Passport', models.CharField(max_length=300)),
                ('Phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.", regex='^(?:\\+)')])),
                ('deposit_paid', models.FloatField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('unit',),
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('unit_number', models.CharField(max_length=300)),
                ('type', models.CharField(choices=[('shop', 'shop'), ('single', 'single'), ('bedsita', 'bedsita'), ('one bedroom', 'one bedroom'), ('two bedroom', 'two bedroom'), ('three bedroom', 'three bedroom'), ('four bedroom', 'four bedroom')], max_length=30, null=True)),
                ('floor_number', models.CharField(choices=[('Ground', 'Ground'), ('Parking-Bay', 'Parking-Bay'), ('zeroth', 'zeroth'), ('first', 'first'), ('second', 'second'), ('third', 'third'), ('fourth', 'fourth'), ('fifth', 'fifth'), ('sixth', 'sixth'), ('seventh', 'seventh'), ('eighth', 'eighth'), ('ninth', 'ninth'), ('tenth', 'tenth'), ('eleventh', 'eleventh'), ('twelfth', 'twelfth'), ('thirteenth', 'thirteenth'), ('fourteenth', 'fourteenth'), ('fifteenth', 'fifteenth'), ('sixteenth', 'sixteenth'), ('seventeenth', 'seventeenth'), ('eighteenth', 'eighteenth'), ('nineteenth', 'nineteenth'), ('twentieth', 'twentieth'), ('twenty-first', 'twenty-first'), ('twenty-second', 'twenty-second'), ('twenty-third', 'twenty-third'), ('twenty-fourth', 'twenty-fourth'), ('twenty-fifth', 'twenty-fifth'), ('twenty-sixth', 'twenty-sixth'), ('twenty-seventh', 'twenty-seventh'), ('twenty-eighth', 'twenty-eighth'), ('twenty-ninth', 'twenty-ninth'), ('thirtieth', 'thirtieth'), ('thirty-first', 'thirty-first'), ('thirty-second', 'thirty-second'), ('thirty-third', 'thirty-third'), ('thirty-fourth', 'thirty-fourth'), ('thirty-fifth', 'thirty-fifth'), ('thirty-sixth', 'thirty-sixth'), ('thirty-seventh', 'thirty-seventh'), ('thirty-eighth', 'thirty-eighth'), ('thirty-ninth', 'thirty-ninth')], max_length=300, null=True)),
                ('monthly_rent', models.FloatField()),
                ('occupied', models.BooleanField(default=False)),
                ('landlord_assigned', models.BooleanField(default=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
            ],
            options={
                'ordering': ('floor_number', 'unit_number', 'property'),
            },
        ),
        migrations.CreateModel(
            name='Transfered_Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('old_unit', models.CharField(max_length=200)),
                ('transfer_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfer_tenant', to='property.Tenant')),
                ('new_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='property.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='tenant',
            name='unit',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='unit_tenant', to='property.Unit'),
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_to_all', models.BooleanField(default=False)),
                ('message', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('tenant', models.ManyToManyField(blank=True, to='property.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=300)),
                ('ID_or_Passport', models.CharField(max_length=300)),
                ('Phone', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.", regex='^(?:\\+)')])),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_landlord', to='property.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039)], default=2020)),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=4)),
                ('Description', models.TextField(max_length=300)),
                ('Amount', models.FloatField()),
                ('Date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('property_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Property')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Damage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('total_cost', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='damages', to='property.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Checked_out_Tenant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(auto_now_add=True, null=True)),
                ('checked_out_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('unit_stayed', models.CharField(max_length=200)),
                ('checked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.Tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=4)),
                ('date_paid', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Date')),
                ('rent', models.FloatField()),
                ('total_amount_paid', models.FloatField(null=True)),
                ('credit', models.FloatField(null=True)),
                ('Balance', models.FloatField(null=True)),
                ('mode_of_payment', models.CharField(choices=[('M-PESA', 'M-PESA'), ('BANK', 'BANK'), ('CASH', 'CASH')], max_length=50, null=True)),
                ('Reciept_no', models.CharField(blank=True, max_length=300, null=True)),
                ('paid', models.BooleanField(default=True)),
                ('service_charge', models.FloatField(default=0)),
                ('year', models.IntegerField(choices=[(1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039)], default=2020)),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='unit_rent', to='property.Unit')),
            ],
            options={
                'ordering': ('-year', 'month', 'unit'),
                'get_latest_by': ('month', 'year'),
                'unique_together': {('unit', 'year', 'month')},
            },
        ),
    ]
