# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from ..lr_app.models import UserDB

# Create your views here.
def index(request):
    return render(request, "books_app/index.html")

def home(request):
    all_users = UserDB.objects.all()
    context = {
    "users": all_users
    }
    return render(request,'books_app/home.html', context)
