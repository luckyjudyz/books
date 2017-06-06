# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import UserDB, BookDB, ReviewDB
# Create your views here.

def log_register(request):
	if request.method == "POST":
		print request.POST
		if request.POST["type"] == "register":
			response = UserDB.objects.check_create(request.POST)
		elif request.POST['type'] == "login":
			response = UserDB.objects.check_log(request.POST)
			if not response[0]:
				for message in response[1]:
					messages.error(request, message[1])
				return redirect('books_app:index')
			else:
				request.session['user'] = {
				"id":response[1].id,
				'username': response[1].username,
				'alios':response[1].alios,
				}
				return redirect('books_app:home')
	return redirect('books_app:index')


def logout(request):
	request.session.clear()
	return redirect('books_app:index')
