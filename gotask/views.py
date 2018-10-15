# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import View
from restraunts.models import myuser,placed_order
from django.utils import timezone
from django.shortcuts import render,redirect

def redirection(request):
    return redirect("/accounts/login/")

def loginhandler(request):
    return render(request, 'login_page.html')

def dashboard(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_obj = myuser.objects.filter(name = username).first()
        current_order = []
        time_left = []
        status = []
        if user_obj:
            total_orders = placed_order.objects.filter(user_id = user_obj.user_id).order_by('-order_time')
            if total_orders:
                for order in total_orders:
                    current_order.append(order)
                    if timezone.now() < (order.order_time+timezone.timedelta(minutes=20)):
                        time_left.append((order.order_time+timezone.timedelta(minutes=20)) - timezone.now())
                        status.append('Being delivered')
                    else:
                        time_left.append('')
                        status.append('Delivered')
        data = zip(current_order,time_left,status)
        return render(request, 'dashboard.html', {'data': data,'username':username})
    else:
        return redirect("/accounts/login/")