import re
import string
import os
import africastalking
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from .models import *
from django.views import generic
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.conf import settings
from .credentials import USERNAME, APIKEY
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import calendar
from django.core.validators import ValidationError
from django.db import IntegrityError

from django.db.models import Sum, Count,Min
import datetime
from utils.helpers import send_sms








@login_required(login_url='/accounts/login/')
def home(request):
    properties = Property.objects.all()
    landlords = Landlord.objects.all()
    tenants = Tenant.objects.filter(active=True)
    units = Unit.objects.all()
    transferred_tenants = Transfered_Tenant.objects.all()
    checked_out_tenants = Checked_out_Tenant.objects.all()
    rents = Rent.objects.all()
    # debtors = Rent.objects.filter(Balance > 0)
    expenses = Expense.objects.all()
    message_ins = IbgaroMessageCounter.objects.get(name='admin')
    messages_count = message_ins.total_messages_sent
    properties_count = properties.count()
    landlords_count = landlords.count()
    tenants_count = tenants.count()
    units_count = units.count()
    transferred_count = transferred_tenants.count()
    checkedout_count = checked_out_tenants.count()
    rent_count = rents.count()
    expenses_count = expenses.count()
    allocated_message = Allocated_message.objects.get(name='admin')
    rem = allocated_message.count
    damages = Damage.objects.all()
    tenants_out = ChekedOutTenant.objects.all()
    property_form = None
    expense_form = None
    unit_form = None
    landlord_form = None
    tenant_form = None
    checkout_form = None
    transfer_form = None
    rent_form = None
    message_form = None
    damage_form = None
    # add property form
    if request.method == 'POST':
        if 'property_button' in request.POST:
            property_form = PropertyForm(data=request.POST)
            if property_form.is_valid():
                property_form.save()
                messages.success(request, "Property added successfully")
                return redirect('property:home')
            if property_form.is_valid() == False:
                property_form = PropertyForm(data=request.POST)
                messages.error(request, "Error adding property, code and name must be unique")
                return redirect('property:home')
    else:
        property_form = PropertyForm()

    # add Unit form
    if request.method == 'POST':
        checker = True
        if 'unit_button' in request.POST:
            unit_form = UnitForm(data=request.POST)
            if unit_form.is_valid():
                property_name = unit_form.cleaned_data['property']
                floor_number = unit_form.cleaned_data['floor_number']
                unit_number = unit_form.cleaned_data['unit_number']
                units = Unit.objects.all()
                for unit in units:
                    if unit.unit_number == unit_number and unit.property == property_name:
                        checker = False
                        messages.error(request, "That unit already exists")
                        unit_form = UnitForm()
                        return redirect('property:home')
                if checker:
                    unit_form.save()
                    messages.success(request, "Unit added successfully")
                    return redirect('property:home')
            else:
                messages.error(request, "Error adding unit")
    else:
        unit_form = UnitForm()

    #damages
    if request.method == 'POST':
        if 'damage_button' in request.POST:
            user = request.user
            damage_form = DamageForm(request.POST)
            if damage_form.is_valid():
                damage = damage_form.save(commit=False)
                damage.recorded_by = user
                damage.save()
                messages.success(request,"damage registered successfully")
                return redirect("property:home")
            else:
                messages.error(request,"Error adding damage")
                damage_form = DamageForm(request.POST)
                return render(request,'property/home.html',{"damage_form":damage_form})

    else:
        damage_form = DamageForm()

    # add LandLord form
    if request.method == 'POST':
        if 'landlord_button' in request.POST:
            landlord_form = LandlordForm(data=request.POST)
            if landlord_form.is_valid():
                unit_selected = landlord_form.cleaned_data['unit']
                unit_selected = str(unit_selected)
                unit_selected = unit_selected.split(' ', 1)[0]
                db_unit = Unit.objects.get(unit_number=unit_selected)
                db_unit.landlord_assigned = True
                db_unit.save()
                landlord_form.save()
                messages.success(request, "Landlord added successfully")
                return redirect('property:home')
            else:
                messages.error(request, "Error adding Landlord")
    else:
        landlord_form = LandlordForm()

    # add Tenant form
    if request.method == 'POST':
        if 'tenant_button' in request.POST:
            tenant_form = TenantForm(data=request.POST)
            if tenant_form.is_valid():
                selected_unit = tenant_form.cleaned_data['unit']
                selected_unit = str(selected_unit)
                selected_unit = selected_unit.split(' ', 1)[0]
                db_unit = Unit.objects.get(unit_number=selected_unit)
                phone = None
                for p in db_unit.unit_landlord.all():
                    phone = p.Phone

                db_unit.occupied = True
                db_unit.save()
                tenant_form.save()
                if phone != None:
                    # sms = africastalking.SMS
                    message = 'You have a new tenant in your house number {}'.format(
                        selected_unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(request, "Tenant added successfully")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                else:
                    messages.success(request, "Tenant added successfully")

                return redirect('property:home')
            else:
                messages.error(
                    request, "Error adding tenant. Same name already exists. Name must be unique")
    else:
        tenant_form = TenantForm()

    # transferred tenant form
    if request.method == 'POST':
        if 'transfer_button' in request.POST:
            transfer_form = TransferredTenantForm(data=request.POST)
            if transfer_form.is_valid():
                tenant = transfer_form.cleaned_data['name']
                new_unit = transfer_form.cleaned_data['new_unit']
                new_transfer_form = transfer_form.save(commit=False)
                db_tenant = Tenant.objects.get(name=tenant)
                new_transfer_form.old_unit = db_tenant.unit
                db_tenant.unit.occupied = False
                db_tenant.unit.save()
                db_tenant.unit = new_unit
                db_tenant.unit.occupied = True
                db_tenant.unit.save()
                db_tenant.save()
                new_transfer_form.save()
                messages.success(request, "Tenant transferred successfully")
                return redirect('property:home')
            else:
                messages.error(request, "Error adding transferred tenant")
    else:
        transfer_form = TransferredTenantForm()
    # checkout tenant form
    if request.method == 'POST':
        if 'checkout_button' in request.POST:
            checkout_form = CheckedOutTenantForm(data=request.POST)
            if checkout_form.is_valid():
                tenant = checkout_form.cleaned_data['name']
                db_tenant = Tenant.objects.get(name=tenant)
                unit = db_tenant.unit
                try:
                    landlord = Landlord.objects.get(unit=unit)
                except Landlord.DoesNotExist:
                    landlord = None
                if landlord:
                    phone = landlord.Phone
                    new_check = checkout_form.save(commit=False)
                    new_check.unit_stayed = db_tenant.unit
                    db_tenant.unit.occupied = False
                    db_tenant.unit.save()
                    db_tenant.active = False
                    db_tenant.save()
                    new_check.save()
                    # sms = africastalking.SMS
                    message = ' tenant in has moved out your house number {}'.format(
                        unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    print(phone)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(
                            request, "Tenant  successfully checked ou")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                else:
                    new_check = checkout_form.save(commit=False)
                    new_check.unit_stayed = db_tenant.unit
                    db_tenant.unit.occupied = False
                    db_tenant.unit.save()
                    db_tenant.active = False
                    db_tenant.save()
                    new_check.save()
                    messages.success(
                        request, "Tenant  successfully checked out")

                return redirect('property:home')
            else:
                messages.error(request, "Error adding checkout tenant")
    else:
        checkout_form = CheckedOutTenantForm()

    # rent form
    if request.method == 'POST':
        if 'rent_button' in request.POST:
            rent_form = RentForm(data=request.POST)
            if rent_form.is_valid():
                tenant = rent_form.cleaned_data['unit']
                db_tenant = Tenant.objects.get(unit=tenant)
                phone = db_tenant.Phone
                rent = rent_form.save(commit=False)
                rent.recorded_by = request.user
                rent.save()
                #sms = africastalking.SMS
                message = 'Thank you for paying your rent\n  Regards Ibgaro Realtors'
                cost = 0
                m = len(message)
                if m <= 144:
                    cost = 1
                elif m <= 304:
                    cost = 2
                elif m <= 464:
                    cost = 3
                elif m <= 624:
                    cost = 4
                elif m <= 784:
                    cost = 5
                message_allocated = Allocated_message.objects.get(name='admin')
                counter = message_allocated.count
                if cost < counter:
                    message_counter = IbgaroMessageCounter.objects.get(
                        name='admin')
                    message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                    message_counter.save()
                    sender = 'softsearch'
                    response = send_sms(message, [phone])
                    counter = counter - cost
                    message_allocated.count = counter
                    message_allocated.save()
                    messages.success(request, "Rent added successfully")
                else:
                    messages.error(
                        request, "You dont have sufficent credit to send messages please recharge")
                return redirect('property:home')
            else:
                messages.error(request, "Error adding rent")
    else:
        rent_form = RentForm()

    # expense form
    if request.method == 'POST':
        if 'expense_button' in request.POST:
            expense_form = ExpenseForm(data=request.POST)
            if expense_form.is_valid():
                expense=expense_form.save(commit=False)
                expense.recorded_by = request.user
                expense.save()
                messages.success(request, "Expense added successfully")
                return redirect('property:home')
            else:
                messages.error(request, "Error adding expense")
    else:
        expense_form = ExpenseForm()
    #messages
    if request.method == 'POST':
        if 'mes' in request.POST:
            message_form = MessagesForm(data=request.POST)
            if message_form.is_valid():
                message = message_form.cleaned_data['message']
                send_to_all = message_form.cleaned_data['send_to_all']
                send_to_all = str(send_to_all)
                if send_to_all == 'True':
                    tenant = Tenant.objects.filter(active=True)
                    #sms = africastalking.SMS
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    message_len = len(message)
                    mes_count = 0
                    che = False
                    for ten in tenant:
                        if message_len <= 144:
                            mes_count = 1
                        elif message_len <= 304:
                            mes_count = 2
                        elif message_len <= 464:
                            mes_count = 3
                        elif message_len <= 624:
                            mes_count = 4
                        elif message_len <= 784:
                            mes_count = 5
                        if mes_count < counter:
                            phone_number = ten.Phone
                            send_sms(message, [phone_number])
                            counter = counter - mes_count
                            message_allocated.count = counter
                            message_allocated.save()
                            message_counter = IbgaroMessageCounter.objects.get(
                                name='admin')
                            message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                            message_counter.save()
                            message_form.save()
                            che = True
                    if che:
                        messages.success(request, "Message sent successfully")

                    else:
                        messages.error(request,
                                       'You don\'t have sufficient credit to send the messages, please recharge')

                else:
                    tenant = message_form.cleaned_data['tenant']
                    print(tenant)
                    if tenant is not None:
                        #sms = africastalking.SMS
                        message_allocated = Allocated_message.objects.get(
                            name='admin')
                        counter = message_allocated.count
                        message_len = len(message)
                        mes_count = 0
                        ches = False
                        for ten in tenant:
                            if message_len <= 144:
                                mes_count = 1
                            elif message_len <= 304:
                                mes_count = 2
                            elif message_len <= 464:
                                mes_count = 3
                            elif message_len <= 624:
                                mes_count = 4
                            elif message_len <= 784:
                                mes_count = 5
                            if mes_count < counter:
                                phone_number = ten.Phone
                                send_sms(message, [phone_number])
                                counter = counter - mes_count
                                message_allocated.count = counter
                                message_allocated.save()
                                message_counter = IbgaroMessageCounter.objects.get(
                                    name='admin')
                                message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                                message_counter.save()
                                message_form.save()
                                ches = True
                            if ches:
                                messages.success(
                                    request, "Message seeeent successfully")
                                return redirect('property:home')

                            else:
                                messages.error(request,
                                               'You don\'t have sufficient credit to send the messages, please recharge')

                    else:
                        messages.error(
                            request, 'Please select at least one tenant')


            else:
                messages.error(request, "Error sending the message")

    else:
        message_form = MessagesForm()
    return render(request, 'property/home.html', {'property_form': property_form,
                                                  'expense_form': expense_form,
                                                  'unit_form': unit_form,
                                                  'rent_form': rent_form,
                                                  'tenant_form': tenant_form,
                                                  'checkout_form': checkout_form,
                                                  'transfer_form': transfer_form,
                                                  'landlord_form': landlord_form,
                                                  "damage_form":damage_form,
                                                  'properties': properties,
                                                  'landlords': landlords,
                                                  'tenants': tenants,
                                                  'units': units,
                                                  'expenses': expenses,
                                                  'checked_out_tenants': checked_out_tenants,
                                                  "tenants_out":tenants_out,
                                                  'transferred_tenants': transferred_tenants,
                                                  'rents': rents,
                                                  'properties_count': properties_count,
                                                  'landlords_count': landlords_count,
                                                  'tenants_count': tenants_count,
                                                  'units_count': units_count,
                                                  'transferred_count': transferred_count,
                                                  'checkedout_count': checkedout_count,
                                                  'rents_count': rent_count,
                                                  'expenses_count': expenses_count,
                                                  'message_form': message_form,
                                                  'messages_count': messages_count,
                                                  'rem': rem

                                                  })


def edit_property(request, id):
    single_property = Property.objects.get(id=id)
    if request.method == 'POST':
        property_form = PropertyForm(
            data=request.POST, instance=single_property)
        if property_form.is_valid():
            property_form.save()
            messages.success(request, "Property updated successfully")
        else:
            messages.error(request, "Error updating property")
    else:
        property_form = PropertyForm(instance=single_property)
    return render(request, 'property/property_edit.html', {'property_form': property_form})


def edit_landlord(request, id):
    single_landlord = Landlord.objects.get(id=id)
    if request.method == 'POST':
        landlord_form = LandlordForm(
            data=request.POST, instance=single_landlord)
        if landlord_form.is_valid():
            landlord_form.save()
            messages.success(request, "Landlord updated successfully")
        else:
            messages.error(request, "Error updating landlord")
    else:
        landlord_form = LandlordForm(instance=single_landlord)
    return render(request, 'property/landlord_edit.html', {'landlord_form': landlord_form})


def edit_tenant(request, id):
    single_tenant = Tenant.objects.get(id=id)
    if request.method == 'POST':
        tenant_form = TenantForm(data=request.POST, instance=single_tenant)
        if tenant_form.is_valid():
            tenant_form.save()
            messages.success(request, "Tenant updated successfully")
        else:
            messages.error(request, "Error updating tenant")
    else:
        tenant_form = TenantForm(instance=single_tenant)
    return render(request, 'property/tenant_edit.html', {'tenant_form': tenant_form})


def edit_unit(request, id):
    single_unit = Unit.objects.get(id=id)
    if request.method == 'POST':
        unit_form = UnitForm(data=request.POST, instance=single_unit)
        if unit_form.is_valid():
            unit_form.save()
            messages.success(request, "Unit updated successfully")
        else:
            messages.error(request, "Error updating unit")
    else:
        unit_form = UnitForm(instance=single_unit)
    return render(request, 'property/edit_unit.html', {'unit_form': unit_form})


def edit_transfer(request, id):
    single_transfer = Transfered_Tenant.objects.get(id=id)
    if request.method == 'POST':
        transfer_form = TransferredTenantForm(
            data=request.POST, instance=single_transfer)
        if transfer_form.is_valid():
            transfer_form.save()
            messages.success(
                request, "Transferred tenant updated successfully")
        else:
            messages.error(request, "Error updating transferred tenant")
    else:
        transfer_form = TransferredTenantForm(instance=single_transfer)
    return render(request, 'property/edit_transfer.html', {'transfer_form': transfer_form})


def edit_checkout(request, id):
    single_checkout = Checked_out_Tenant.objects.get(id=id)
    if request.method == 'POST':
        checkout_form = CheckedOutTenantForm(
            data=request.POST, instance=single_checkout)
        if checkout_form.is_valid():
            checkout_form.save()
            messages.success(request, "Checkout tenant updated successfully")
        else:
            messages.error(request, "Error updating checkout tenant")
    else:
        checkout_form = CheckedOutTenantForm(instance=single_checkout)
    return render(request, 'property/edit_checkout.html', {'checkout_form': checkout_form})


def edit_rent(request, id):
    single_rent = Rent.objects.get(id=id)
    if request.method == 'POST':
        rent_form = RentForm(data=request.POST, instance=single_rent)
        if rent_form.is_valid():
            rent_form.save()
            messages.success(request, "Rent updated successfully")
        else:
            messages.error(request, "Error updating Rent")
    else:
        rent_form = RentForm(instance=single_rent)
    return render(request, 'property/edit_rent.html', {'rent_form': rent_form})












def edit_expense(request, id):
    single_expense = Expense.objects.get(id=id)
    if request.method == 'POST':
        expense_form = ExpenseForm(data=request.POST, instance=single_expense)
        if expense_form.is_valid():
            expense_form.save()
            messages.success(request, "Expense updated successfully")
        else:
            messages.error(request, "Error updating expense")
    else:
        expense_form = ExpenseForm(instance=single_expense)
    return render(request, 'property/edit_expense.html', {'expense_form': expense_form})


def edit_damage(request, id):
    damage = Damage.objects.get(id=id)
    if request.method == 'POST':
        damage_form = DamageForm(data=request.POST, instance=damage)
        if damage_form.is_valid():
            damage_form.save()
            messages.success(request, "Damage updated successfully")
        else:
            messages.error(request, "Error updating Damage")
    else:
        damage_form = DamageForm(instance=damage)
    return render(request, 'property/edit_damage.html', {'damage_form': damage_form})


def delete_property(request, id):
    single_property = Property.objects.get(id=id)
    single_property.delete()
    messages.success(request, "Property deleted successfully")
    return redirect('property:home')

def delete_damage(request, id):
    damage = Damage.objects.get(id=id)
    damage.delete()
    messages.success(request, "Damages deleted successfully")
    return redirect('property:home')

def delete_landlord(request, id):
    single_landlord = Landlord.objects.get(id=id)
    single_landlord.delete()
    messages.success(request, "Landlord deleted successfully")
    return redirect('property:home')


def delete_tenant(request, id):
    single_tenant = Tenant.objects.get(id=id)
    db_unit = Unit.objects.get(id=single_tenant.unit.id)
    db_unit.occupied = False
    db_unit.save()
    single_tenant.delete()
    messages.success(request, "Tenant deleted successfully")
    return redirect('property:home')


def delete_unit(request, id):
    user = request.user
    single_unit = Unit.objects.get(id=id)
    if user.is_superuser:
        single_unit.delete()
        messages.success(request, "Unit deleted successfully")
        return redirect('property:home')

    if user.is_superuser == False:
        messages.error(request, "you dont have permision to perfom this")
        return redirect('property:home')



def delete_checkout(request, id):
    single_checkout = Checked_out_Tenant.objects.get(id=id)
    single_checkout.delete()
    messages.success(request, "Checkout tenant deleted successfully")
    return redirect('property:home')


def delete_transfer(request, id):
    single_transfer = Transfered_Tenant.objects.get(id=id)
    single_transfer.delete()
    messages.success(request, "Transfer tenant deleted successfully")
    return redirect('property:home')


def delete_rent(request, id):
    single_rent = Rent.objects.get(id=id)
    single_rent.delete()
    messages.success(request, "Rent deleted successfully")
    return redirect('property:home')


def delete_expense(request, id):
    single_expense = Expense.objects.get(id=id)
    single_expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect('property:home')

def delete_checked_tenant(request,id):
    single_ten = ChekedOutTenant.objects.get(id=id)
    single_ten.delete()
    messages.success(request, "checked out tenant deleted successfully")
    return redirect('property:home')



class PropertyDetail(generic.DetailView):
    model = Property
    template_name = 'property/property_detail.html'


class LandlordDetail(generic.DetailView):
    model = Landlord
    template_name = 'property/landlord_detail.html'


class UnitDetail(generic.DetailView):
    model = Unit
    template_name = 'property/unit_detail.html'


class TenantDetail(generic.DetailView):
    model = Tenant
    template_name = 'property/tenant_detail.html'


class Transfered_TenantDetail(generic.DetailView):
    model = Transfered_Tenant
    template_name = 'property/transferedtenant_detail.html'


class Checkout_TenantDetail(generic.DetailView):
    model = Checked_out_Tenant
    template_name = 'property/checkout_detail.html'


class RentDetail(generic.DetailView):
    model = Rent
    template_name = 'property/rent_detail.html'

def rent_detail(request,id):## TODO:
    """single unit rent"""
    unit = Unit.objects.get(id=id)
    rents = Rent.objects.filter(unit=unit)
    return render(request,'property/unit_rent_report.html',{"rents":rents,"unit":unit})


def single_tenant_damages(request,id):
    """display damages recorded against single tenant"""
    tenant = Tenant.objects.get(id=id)
    return render(request,'property/tenant_damages.html',{'tenant':tenant})



class ExpenseDetail(generic.DetailView):
    model = Expense
    template_name = 'property/expense_detail.html'


def detailed_property_report(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(property__name=property.name)
    return render(request, 'property/detailed_property_report.html', {'units': units})


def send_reminder_sms(request):
    return render(request, 'property/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            return redirect('property:home')
    else:
        form = SignUpForm()
    return render(request, 'property/signup.html', {'form': form})

#adding rent
def add_rent(request, id):
    rent_form = None
    unit = Unit.objects.get(id=id)
    if request.method == 'POST':
        if 'rent_button' in request.POST:
            rent_form = RentForm(data=request.POST)
            if rent_form.is_valid():
                rent= rent_form.cleaned_data['rent']
                month = rent_form.cleaned_data['month']
                year = rent_form.cleaned_data['year']
                rent = str(rent)
                rent = float(rent)
                new_rent_form = rent_form.save(commit=False)
                tenant = Tenant.objects.get(unit=unit)
                phone = tenant.Phone
                name = tenant.name
                monthly_rent = unit.monthly_rent
                balance = monthly_rent - rent
                if rent > monthly_rent:
                    credit = rent - monthly_rent
                new_rent_form.unit = unit
                new_rent_form.recorded_by = request.user
                try:#using try chatch to find out if rent for that partcular period is allready recorded
                    Rent.objects.get(year=year,month=month,unit=unit )
                except Rent.DoesNotExist:
                    pass
                else:
                    messages.error(request,'rent record for this month already exists, unless you want to eddit to clear balance ')
                    rent_form = RentForm(request.POST,instance=new_rent_form)
                    return redirect('property/add_rent.html', {'rent_form': rent_form})

                new_rent_form.save()
                #sms = africastalking.SMS
                if rent <= monthly_rent:
                    message = 'Dear {}, we thank you for paying your rent Ksh.{} for month of {}/{},\nBalance ksh.{}\n  Regards Softsearch Realtors.'.format(
                        name, rent, month, year, balance)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(name='admin')
                    counter = message_allocated.count
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(request, "Rent added successfully")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                    return redirect('property:home')
                if rent > monthly_rent:
                    message = 'Dear {}, we thank you for paying your rent Ksh.{} for month of {}/{},\ncredit carried forward ksh.{}\n  SoftsearchLimited Realtors.'.format(
                        name, rent, month, year, credit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(name='admin')
                    counter = message_allocated.count
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(request, "Rent added successfully")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                    return redirect('property:home')
                else:
                    messages.error(request, "Error adding rent")
    else:
        rent_form = RentForm()
    return render(request, 'property/add_rent.html', {'rent_form': rent_form})


def detailed_property_rent(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(property__name=property.name, occupied=True)
    return render(request, 'property/detailed_property_rent.html', {'units': units})


def add_landlord(request, id):
    landlord_form = None
    unit = Unit.objects.get(id=id)
    if request.method == 'POST':
        if 'landlord_button' in request.POST:
            landlord_form = LandlordForm(data=request.POST)
            if unit.landlord_assigned == True:
                messages.error(request, "Landlord already assigned to the unit")
                return redirect('property:home')
            if landlord_form.is_valid():
                new_land_form = landlord_form.save(commit=False)
                unit = Unit.objects.get(id=unit.id)
                unit.landlord_assigned = True
                unit.save()
                new_land_form.unit = unit
                new_land_form.save()
                messages.success(request, "Landlord added successfully")
                return redirect('property:home')
            else:
                messages.error(request, "Error adding Landlord")
    else:
        landlord_form = LandlordForm()
    return render(request, 'property/add_landlord.html', {'landlord_form': landlord_form})


def detailed_property_landlord(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(
        property__name=property.name, landlord_assigned=False).order_by('-date_added',)
    return render(request, 'property/detailed_property_landlord.html', {'units': units})


def add_tenant(request, id):
    unit = Unit.objects.get(id=id)
    tenant_form = None
    if request.method == 'POST':
        if 'tenant_button' in request.POST:
            tenant_form = TenantForm(data=request.POST)
            if unit.occupied ==True:
                tenant_form = TenantForm(data=request.POST)
                messages.error(request, "Unit is occupied")
                return render(request, 'property/add_tenant.html', {'tenant_form': tenant_form})
            if tenant_form.is_valid():
                new_tenant_form = tenant_form.save(commit=False)
                phone = None
                name = None
                for p in unit.unit_landlord.all():
                    phone = p.Phone
                    name = p.name
                unit.occupied = True
                unit.save()
                new_tenant_form.unit = unit
                new_tenant_form.registered_by = request.user
                new_tenant_form.save()
                if phone != None:
                    #sms = africastalking.SMS
                    message = 'Dear {},You have a new tenant in your house number {},\n SoftsearchLimited Realtors.'.format(
                        name, unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(request, "Tenant added successfully")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                else:
                    messages.success(request, "Tenant added successfully")

                return redirect('property:home')
            else:
                messages.error(
                    request, "some  incorrect input")
    else:
        tenant_form = TenantForm()
    return render(request, 'property/add_tenant.html', {'tenant_form': tenant_form})


def detailed_property_tenant(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(property__name=property.name, occupied=False)
    return render(request, 'property/detailed_property_tenant.html', {'units': units})


def add_transferred_tenant(request, id):
    transfer_form = None
    phone = None
    phone1 = None
    unit = Unit.objects.get(id=id)
    if request.method == 'POST':
        if 'transfer_button' in request.POST:
            transfer_form = TransferredTenantForm(data=request.POST)
            if transfer_form.is_valid():
                tenant = Tenant.objects.get(unit=unit)
                tenant = tenant.name
                new_unit = transfer_form.cleaned_data['new_unit']
                new_transfer_form = transfer_form.save(commit=False)
                db_tenant = Tenant.objects.get(name=tenant)
                new_transfer_form.old_unit = db_tenant.unit
                new_transfer_form.name = db_tenant
                db_tenant.unit.occupied = False
                for p in db_tenant.unit.unit_landlord.all():  # old landlord number
                    phone = p.Phone
                    name = p.name
                for p in new_unit.unit_landlord.all():  # new landlord number
                    phone1 = p.Phone
                    name1 = p.name
                db_tenant.unit.save()
                db_tenant.unit = new_unit
                db_tenant.unit.occupied = True
                db_tenant.unit.save()
                db_tenant.save()
                new_transfer_form.save()
                cheker1 = False
                if phone != None:  # send text to privious LandLord
                    #sms = africastalking.SMS
                    message = 'Dear {},tenant has been transferred out of your unit number {}\n Regards SoftsearchLimited.'.format(
                        name, unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        cheker1 = True
                        # messages.success(request, "Tenant transfered successfully")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")

                else:
                    messages.success(
                        request, "Tenant transferred successfully")
                cheker2 = False
                if phone1 != None:  # send text to new LandLord
                    #sms = africastalking.SMS
                    message = 'Dear {},tenant has been transferred into your unit number {}\n Regards SoftsearchLimited.'.format(
                        name1, new_unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        cheker2 = True
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                if cheker1 and cheker2:
                    messages.success(
                        request, "Tenant transferred successfully")
                    return redirect('property:home')



            else:
                messages.error(request, "Error adding transferred tenant")
    else:
        transfer_form = TransferredTenantForm()
    return render(request, 'property/add_transfer.html', {'transfer_form': transfer_form})


def detailed_property_transfer(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(property__name=property.name, occupied=True)
    return render(request, 'property/detailed_property_transfer.html', {'units': units})


def add_checkout(request, id):
    checkout_form = None
    unit = Unit.objects.get(id=id)
    date_data = datetime.datetime.now()
    date = date_data.strftime("%d,%B,%Y")
    if request.method == 'POST':
        if 'checkout_button' in request.POST:
            checkout_form = CheckedOutTenantForm(data=request.POST)
            if checkout_form.is_valid():
                tenant = Tenant.objects.get(unit=unit)
                tenant = tenant.name
                db_tenant = Tenant.objects.get(name=tenant)
                unit = db_tenant.unit
                ten=ChekedOutTenant.objects.create(name=tenant,checked_by=request.user,unit=unit,date=date)
                print(ten)
                try:
                    landlord = Landlord.objects.get(unit=unit)
                except Landlord.DoesNotExist:
                    landlord = None
                if landlord:
                    phone = landlord.Phone
                    name = landlord.name
                    new_check = checkout_form.save(commit=False)
                    new_check.unit_stayed = db_tenant.unit
                    new_check.name = db_tenant
                    new_check.checked_by = request.user
                    # db_tenant.unit.occupied = False
                    # db_tenant.unit.save()
                    new_unit = Unit.objects.create(
                        property=unit.property, floor_number=unit.floor_number, monthly_rent=unit.monthly_rent, unit_number=unit.unit_number)
                    Landlord.objects.create(
                        name=landlord.name, ID_or_Passport=landlord.ID_or_Passport, Phone=landlord.Phone, unit=new_unit)
                    ##capturinng the Checked_out_Tenant
                    new_check.save()
                    db_tenant.unit.delete()
                    #sms = africastalking.SMS
                    message = 'Dear {} tenant has moved out your house number {}\n Regards SoftsearchLimited.'.format(
                        name, unit)
                    cost = 0
                    m = len(message)
                    if m <= 144:
                        cost = 1
                    elif m <= 304:
                        cost = 2
                    elif m <= 464:
                        cost = 3
                    elif m <= 624:
                        cost = 4
                    elif m <= 784:
                        cost = 5
                    message_allocated = Allocated_message.objects.get(
                        name='admin')
                    counter = message_allocated.count
                    print(counter)
                    print(phone)
                    if cost < counter:
                        message_counter = IbgaroMessageCounter.objects.get(
                            name='admin')
                        message_counter.total_messages_sent = message_counter.total_messages_sent + 1
                        message_counter.save()
                        sender = 'softsearch'
                        response = send_sms(message, [phone])
                        counter = counter - cost
                        message_allocated.count = counter
                        message_allocated.save()
                        messages.success(
                            request, "Tenant  successfully checked out")
                    else:
                        messages.error(
                            request, "You dont have sufficent credit to send messages please recharge")
                else:
                    new_check = checkout_form.save(commit=False)
                    new_check.unit_stayed = db_tenant.unit
                    new_check.name = db_tenant
                    new_unit = Unit.objects.create(
                        property=unit.property, floor_number=unit.floor_number, monthly_rent=unit.monthly_rent, unit_number=unit.unit_number)
                    new_check.save()
                    db_tenant.unit.delete()
                    messages.success(
                        request, "Tenant  successfully checked out")

                return redirect('property:home')
            else:
                messages.error(request, "Error adding checkout tenant")
    else:
        checkout_form = CheckedOutTenantForm()
    return render(request, 'property/add_checkout.html', {'checkout_form': checkout_form})



def detailed_property_checkout(request, id):
    property = Property.objects.get(id=id)
    units = Unit.objects.filter(property__name=property.name, occupied=True)
    return render(request, 'property/detailed_property_checkout.html', {'units': units})

def property_financial_statement(request, id):
    """financial collecton on monthly basis for partcular property"""

    property = Property.objects.get(id=id)
    qs = Rent.objects.filter(unit__property=property)
    report = qs.values('year','month').order_by('-year','month').annotate(Sum('rent'),Sum('service_charge'),Sum('total_amount_paid'),Sum('Balance'),Count('pk'))
    return render(request, 'property/financial_statement.html', {'report': report,'property':property})







def property_financial_summary(request):
    """financial collecton on monthly basis for all properties """
    qs = Rent.objects.all()
    report = qs.values('year','month').order_by('-year','month').annotate(Sum('rent'),Sum('service_charge'),Sum('total_amount_paid'),Sum('Balance'),Count('pk'))
    return render(request, 'property/financial_summary.html', {'report': report})
