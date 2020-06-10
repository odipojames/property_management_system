from __future__ import unicode_literals
from django.utils.dates import MONTHS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import date
import datetime
from django.core.validators import RegexValidator
from num2words import num2words
from django.core.validators import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from . helpers import enforce_all_required_arguments_are_truthy

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom manager to handle the User model methods.
    """

    def create_user(
        self, full_name=None, email=None, password=None, phone=None, role=None, **kwargs
    ):
        REQUIRED_ARGS = ("full_name", "email", "password", "phone")

        enforce_all_required_arguments_are_truthy(
            {
                "full_name": full_name,
                "email": email,
                "password": password,
                "phone": phone,
            },
            REQUIRED_ARGS,
        )
        # ensure that the passwords are strong enough.
        try:
            password_validation.validate_password(password)
        except ValidationError as exc:
            # return error accessible in the appropriate field, ie password
            raise ValidationError({"password": exc.messages}) from exc

        user = self.model(
            full_name=full_name,
            email=self.normalize_email(email),
            phone=phone,
            **kwargs
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, full_name=None, email=None, password=None, phone=None, role=None, **kwargs
    ):
        """
        This is the method that creates superusers in the database.
        """

        admin = self.create_user(
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            is_superuser=True,
            is_active = True,
            is_staff = True
        )

        return admin

class User(PermissionsMixin,AbstractBaseUser):
    """
    Custom user model to be used throughout the application.
    """

    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(regex=r'^(?:\+)', message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=15,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["full_name", "phone"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):

        return self.get_username()

    @property
    def get_email(self):

        return self.email

    @property
    def get_full_name(self):
        return self.full_name

    @property
    def get_phone(self):
        return self.phone

    def save(self, *args, **kwarg):
        self.email = self.get_email
        self.full_name = self.get_full_name
        self.phone = self.get_phone
        super(User, self).save(*args, **kwarg)


class Property(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300, unique=True)
    code = models.CharField(max_length=300, unique=True)
    location = models.CharField(max_length=300)
    number_of_units = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    number_of_floors =models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):

        return self.name


class Unit(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=300)
    TYPE_CHOICES = [('shop', 'shop'),('single', 'single'),
    ('bedsita', 'bedsita'),('one bedroom', 'one bedroom'),('two bedroom', 'two bedroom'),('three bedroom', 'three bedroom'),('four bedroom', 'four bedroom'),]
    type = models.CharField(max_length=30,choices=TYPE_CHOICES,null =True)
    floor_CHOICES = [('Ground', 'Ground'),
    ('Parking-Bay', 'Parking-Bay'),]
    for r in range(40):
        floor_CHOICES.append((num2words(r,to='ordinal'),num2words(r, to='ordinal')))
    floor_number =models.CharField(max_length=300,null=True,choices=floor_CHOICES)
    monthly_rent = models.FloatField()
    occupied = models.BooleanField(default=False)
    landlord_assigned = models.BooleanField(default=False)

    class Meta:
        ordering = ('floor_number','unit_number','property',)

    def __str__(self):

        return '{} of {}'.format(self.unit_number, self.property)


class Landlord(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300)
    ID_or_Passport = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^(?:\+)', message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.")
    Phone = models.CharField(validators=[phone_regex], max_length=15,null=True)
    unit = models.ForeignKey(Unit, related_name='unit_landlord', on_delete=models.CASCADE)

    def __str__(self):

        return self.name


class Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.CharField(max_length=300,null=True)
    ID_or_Passport = models.CharField(max_length=300)
    phone_regex = RegexValidator(regex=r'^(?:\+)', message="Phone number must be entered in the format: '+2549999999'. Up to 15 digits allowed.")
    Phone = models.CharField(max_length=15, validators=[phone_regex])
    unit = models.OneToOneField(Unit, related_name='unit_tenant', on_delete=models.CASCADE)
    deposit_paid = models.FloatField()
    active = models.BooleanField(default=True)
    registered_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ('unit',)

    def __str__(self):
        return '{} from unit {}'.format(self.name, self.unit)


class Transfered_Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Tenant, on_delete=models.CASCADE,related_name='transfer_tenant')
    old_unit = models.CharField(max_length=200)
    new_unit = models.ForeignKey(Unit, on_delete=models.CASCADE,related_name='units')
    transfer_date = models.DateField(("Date"), default=date.today)

    def __str__(self):
        return self.name


class Checked_out_Tenant(models.Model):
    date_added = models.DateField(auto_now_add=True, null=True)
    name = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    checked_out_date = models.DateField(("Date"), default=date.today)
    unit_stayed = models.CharField(max_length=200)
    checked_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):

        return self.name


class Rent(models.Model):
    PAYMENT = (
        ('M-PESA', 'M-PESA'),
        ('BANK', 'BANK'),
        ('CASH', 'CASH')
    )
    choices = [(k, v) for k, v in MONTHS.items()]
    month = models.IntegerField(choices=choices,default=datetime.datetime.now().month)
    date_paid = models.DateField(("Date"), default=date.today,null=True,blank=True)
    unit = models.ForeignKey(Unit,on_delete=models.CASCADE,null=True,related_name='unit_rent')
    rent = models.FloatField()
    total_amount_paid = models.FloatField(null = True)
    credit = models.FloatField(null=True)
    Balance = models.FloatField(null=True)
    mode_of_payment = models.CharField(max_length=50, choices=PAYMENT, null=True)
    Reciept_no = models.CharField(max_length=300,blank=True,null=True)
    paid = models.BooleanField(default=True)
    service_charge = models.FloatField(default=0)
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

    year = models.IntegerField(choices=YEAR_CHOICES,
           default=datetime.datetime.now().year)
    recorded_by = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
         unique_together = [("unit", "year","month")]
         ordering = ('-year','month','unit')
         get_latest_by = ('month','year',)

    @property
    def get_balance(self):
        if self.rent < self.unit.monthly_rent:
            Balance = self.unit.monthly_rent - self.rent
        else:
            Balance = 0
        return Balance

    @property
    def get_credit(self):
        if self.rent > self.unit.monthly_rent :
            credit = self.rent - self.unit.monthly_rent
        else:
            credit = 0

        return credit

    @property
    def get_total_amount_paid(self):
        total_amount_paid = self.rent + self.service_charge
        return total_amount_paid


    def save(self, *args, **kwarg):
        self.total_amount_paid = self.get_total_amount_paid
        self.Balance = self.get_balance
        self.credit = self.get_credit
        super(Rent, self).save(*args, **kwarg)




class Expense(models.Model):
    YEAR_CHOICES = []
    for r in range(1980, (datetime.datetime.now().year+20)):
        YEAR_CHOICES.append((r,r))

    year = models.IntegerField(choices=YEAR_CHOICES,
           default=datetime.datetime.now().year)
    choices = [(k, v) for k, v in MONTHS.items()]
    month = models.IntegerField(choices=choices,default=datetime.datetime.now().month)
    property_code = models.ForeignKey(Property,on_delete=models.CASCADE)
    Description = models.TextField(max_length=300)
    Amount = models.FloatField()
    Date = models.DateField(("Date"), default=date.today)
    recorded_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.Amount)


class Messages(models.Model):
    send_to_all = models.BooleanField(default=False)
    tenant = models.ManyToManyField(Tenant, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.message


class Allocated_message(models.Model):
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class IbgaroMessageCounter(models.Model):
    name = models.CharField(max_length=200, null=True)
    total_messages_sent = models.PositiveIntegerField()


class Damage(models.Model):
    tenant = models.ForeignKey(Tenant,on_delete=models.CASCADE,related_name='damages')
    description = models.CharField(max_length = 200)
    total_cost = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date',)
        get_latest_by = ('date')


    def __str__(self):
        return f'Ksh. {self.total_cost}'


class ChekedOutTenant(models.Model):
    """to store chaked out tenants"""
    name = models.CharField(max_length = 200)
    checked_by = models.CharField(max_length = 200)
    unit = models.CharField(max_length=200)
    date = models.CharField(max_length=200)

    def __str__(self):
        return self.name
