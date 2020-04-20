from django.urls import re_path,path

from . import views
from .views import signup_view



app_name = 'property'


urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^delete/property/(?P<id>\d+)/', views.delete_property, name='property'),
    re_path(r'^delete/landlord/(?P<id>\d+)/', views.delete_landlord, name='landlord'),
    re_path(r'^delete/tenant/(?P<id>\d+)/', views.delete_tenant, name='tenant'),
    re_path(r'^delete/unit/(?P<id>\d+)/', views.delete_unit, name='unit'),
    re_path(r'^delete/transferred/tenant/(?P<id>\d+)/', views.delete_transfer, name='transfer'),
    re_path(r'^delete/checked/out/tenant/(?P<id>\d+)/', views.delete_checkout, name='checkout'),
    re_path(r'^delete/rent/(?P<id>\d+)/', views.delete_rent, name='rent'),
    re_path(r'^delete/expense/(?P<id>\d+)/', views.delete_expense, name='expense'),
    re_path(r'^edit/expense/(?P<id>\d+)/', views.edit_expense, name='edit_expense'),
    re_path(r'^edit/property/(?P<id>\d+)/', views.edit_property, name='edit_property'),
    re_path(r'^edit/landlord/(?P<id>\d+)/', views.edit_landlord, name='edit_landlord'),
    re_path(r'^edit/tenant/(?P<id>\d+)/', views.edit_tenant, name='edit_tenant'),
    re_path(r'^edit/unit/(?P<id>\d+)/', views.edit_unit, name='edit_unit'),
    re_path(r'^edit/transfer/tenant/(?P<id>\d+)/', views.edit_transfer, name='edit_transfer'),
    re_path(r'^edit/checkout/(?P<id>\d+)/', views.edit_checkout, name='edit_checkout'),
    re_path(r'^edit/rent/(?P<id>\d+)/', views.edit_rent, name='edit_rent'),
    path('property/<int:pk>/', views.PropertyDetail.as_view(), name='property_detail'),
    path('unit/<int:pk>/', views.UnitDetail.as_view(), name='unit_detail'),
    path('landlord/<int:pk>/', views.LandlordDetail.as_view(), name='landlord_detail'),
    path('tenant/<int:pk>/', views.TenantDetail.as_view(), name='tenant_detail'),
    path('transferedtenants/<int:pk>/', views.Transfered_TenantDetail.as_view(), name='transferedtenants_detail'),
    path('checkouttenants/<int:pk>/', views.UnitDetail.as_view(), name='checkouttenants_detail'),
    path('rent/<int:pk>/', views.RentDetail.as_view(), name='rent_detail'),
    path('expenses/<int:pk>/', views.ExpenseDetail.as_view(), name='expense_detail'),
    re_path('signup/',views.signup_view, name="signup"),
    re_path(r'^detailed/property/(?P<id>\d+)/', views.detailed_property_report, name='detailed_property_report'),
    re_path(r'^detailed/property/rent/(?P<id>\d+)/', views.detailed_property_rent, name='detailed_property_rent'),
    re_path(r'^add/rent/(?P<id>\d+)/', views.add_rent, name='add_rent'),
    re_path(r'^detailed/property/landlord/(?P<id>\d+)/', views.detailed_property_landlord, name='detailed_property_landlord'),
    re_path(r'^add/landlord/(?P<id>\d+)/', views.add_landlord, name='add_landlord'),
    re_path(r'^detailed/property/tenant/(?P<id>\d+)/', views.detailed_property_tenant, name='detailed_property_tenant'),
    re_path(r'^add/tenant/(?P<id>\d+)/', views.add_tenant, name='add_tenant'),
    re_path(r'^detailed/property/transfer/(?P<id>\d+)/', views.detailed_property_transfer, name='detailed_property_transfer'),
    re_path(r'^add/transfer/(?P<id>\d+)/', views.add_transferred_tenant, name='add_transfer'),
    re_path(r'^detailed/property/checkout/(?P<id>\d+)/', views.detailed_property_checkout, name='detailed_property_checkout'),
    re_path(r'^add/checkout/(?P<id>\d+)/', views.add_checkout, name='add_checkout'),
    path('unit/rent/<int:id>',views.rent_detail,name='single_unit_rent'),
    path('fin/statement/<int:id>',views.property_financial_statement,name='statement'),
    path('fin/statement/',views.property_financial_summary,name='summary_report'),

]
