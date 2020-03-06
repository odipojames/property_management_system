# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Property

# Create your tests here.


class PropertyTest(TestCase):

    def setUp(self):
        self.obj1 = Property(name='Simwata', code='2344w', number_of_units=33,
                             number_of_floors=3, date_added='12/2019', location='eastley')

    def test_instant(self):

        self.assertTrue(isinstance(self.obj1, Property))

    def test_create_property(self):
        obj = Property.objects.create(name='Sima',code='233',number_of_units=12,number_of_floors=3,date_added='12/2018',location='Eastley')

        obj2=Property.objects.get(code='233')
        self.assertTrue(obj2.name,'Sima')

    def test_delete(self):
        obj =  Property.objects.create(name='Simwata', code='2344w', number_of_units=33,
                             number_of_floors=3, date_added='12/2019', location='eastley')
        obj = Property.objects.get(id=obj.id)
        obj.delete()

        self.assertTrue(obj.name,None)
