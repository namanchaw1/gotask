# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,redirect
from models import restraunts,dishe,placed_order,myuser
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        if myuser.objects.filter(name=username).first()== None:
            user_list = myuser.objects.all()
            userid = len(user_list)+1
            email = str(username)+"@example.com"
            data = myuser(user_id = userid,name = username,email = email)
            data.save()
        res = restraunts.objects.all()
        restraunt_name=[]
        place = []
        id = []
        if res:
            for restraunt in res:
                restraunt_name.append(restraunt.restraunt_name)
                place.append(restraunt.restraunt_place)
                id.append(restraunt.restraunt_id)
        data = zip(restraunt_name,place,id)
        return render(request,'home.html',{'data': data,'username':username})
    else:
        return redirect("/accounts/login/")

def menu(request,id):
    if request.user.is_authenticated:
        username = request.user.username
        rest = restraunts.objects.filter(restraunt_id=id)
        instance = dishe.objects.filter(restraunt_id = rest)
        price = []
        dish_name = []
        value = []
        csrftoken = request.COOKIES.get('csrftoken')
        # import pdb
        # pdb.set_trace()
        if instance:
            for dish in instance:
                price.append(dish.dish_price)
                dish_name.append(dish.dish_name)
                value.append(dish.dish_id)
                data = zip(dish_name, price,value)
            return render(request, 'menu.html', {'data': data,'csrftoken':csrftoken})
        else:
            return render(request, '404.html')
    else:
        return redirect("/accounts/login/")

def placeorder(request):
    username = request.user.username
    user = myuser.objects.filter(name=username).first()
    neworder = placed_order.objects.create(user_id = user.user_id)

    #EMAIL WILL NOT BE SENT BECAUSE I HAVE REMOVED MY PASSWORD FROM settings.py
    subject = 'New Order'
    message = 'Hi, you have placed an order with orderID:' + str(neworder.order_id)
    email_from = settings.EMAIL_HOST_USER
    email_to = [user.email,settings.EMAIL_HOST_USER]

    send_mail(subject,message,email_from,email_to,fail_silently=True)

    return HttpResponse('<html><body>SUCCESS!</body></html>')



