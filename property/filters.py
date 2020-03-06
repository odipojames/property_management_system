from django.contrib.auth.models import User
from .models import Property, Landlord, Tenant, Transfered_Tenant, Checked_out_Tenant, Rent, Expense, Unit
import django_filters


class PropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = ('name', 'code', 'location', 'number_of_units', 'number_of_floors')   

            