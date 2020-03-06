# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Property)


class LandlordAdmin(admin.ModelAdmin):
    list_display = ['name', 'Phone', 'date_added']


admin.site.register(Landlord, LandlordAdmin)


class MessagesAdmin(admin.ModelAdmin):
    list_display = ['total_messages_sent']


admin.site.register(IgbaroMessageCounter, MessagesAdmin)

admin.site.register(Allocated_message)
