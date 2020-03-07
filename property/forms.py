from django import forms
from .models import Property, Landlord, Tenant, Transfered_Tenant, Checked_out_Tenant, Rent, Expense, Unit, Messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.dates import MONTHS
from django.core.validators import RegexValidator
from datetime import date
import datetime
from num2words import num2words
from django.core.validators import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
import calendar

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('name', 'code', 'location', 'number_of_units', 'number_of_floors')


class LandlordForm(forms.ModelForm):
    Phone = forms.CharField(min_length=10)

    class Meta:
        model = Landlord
        fields = ('name', 'id', 'ID_or_Passport', 'Phone')


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        fields = ('property', 'unit_number','type', 'floor_number', 'monthly_rent')


class TenantForm(forms.ModelForm):
    Phone = forms.CharField(min_length=10)

    class Meta:
        model = Tenant
        fields = ('name', 'id', 'ID_or_Passport', 'Phone', 'deposit_paid')






class TransferredTenantForm(forms.ModelForm):
    class Meta:
        model = Transfered_Tenant
        fields = ('new_unit', 'transfer_date')

    def __init__(self, *args, **kwargs):
        super(TransferredTenantForm, self).__init__(*args, **kwargs)
        try:
            self.fields['new_unit'].queryset = Unit.objects.filter(occupied=False)
        except Unit.DoesNotExist:
            ### there is not userextend corresponding to this user, do what you want
            raise Exception('object does not exist')
            pass


class CheckedOutTenantForm(forms.ModelForm):
    class Meta:
        model = Checked_out_Tenant
        fields = ('checked_out_date',)


class RentForm(forms.ModelForm):
    Reciept_no = forms.CharField(label='Receipt Number or Transaction ID',required = False)

    class Meta:
        model = Rent
        fields = ('rent', 'service_charge', 'month','year','date_paid', 'mode_of_payment', 'Reciept_no')






class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('property_code', 'year','month','Description', 'Amount', 'Date')


class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('send_to_all', 'tenant', 'message',)

    def __init__(self, *args, **kwargs):
        super(MessagesForm, self).__init__(*args, **kwargs)
        try:
            self.fields['tenant'].queryset = Tenant.objects.filter(active=True)
        except Unit.DoesNotExist:
            ### there is not userextend corresponding to this user, do what you want
            raise Exception('object does not exist')
            pass



class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username' ,'email', 'password1','password2' )
