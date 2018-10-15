# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class myuser(models.Model):
    user_id = models.IntegerField(primary_key=True,db_index= True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class restraunts(models.Model):
    restraunt_id = models.IntegerField(primary_key=True,db_index= True,default=uuid.uuid4)
    restraunt_name = models.CharField(max_length=100)
    restraunt_place = models.CharField(max_length=100)

class dishe(models.Model):
    restraunt_id = models.ForeignKey(restraunts,on_delete=models.CASCADE,db_index= True,default=uuid.uuid4)
    dish_id = models.IntegerField(unique=True, default=uuid.uuid4)
    dish_name = models.CharField(max_length=100)
    dish_price = models.IntegerField()

class placed_order(models.Model):
    user_id = models.IntegerField(db_index= True,)
    order_id = models.AutoField(unique = True,primary_key=True)
    order_time = models.DateTimeField(default = timezone.now())


