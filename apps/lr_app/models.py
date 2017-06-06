# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re
EMAILREG = re.compile(r'[a-zA-Z0-9.-_+]+@[a-zA-Z0-9.-_+]+\.[a-zA-Z]*$')

# Create your models here.

class userDBManager(models.Manager):
    def hash_pass(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    def check_create(self, data):
        errors = []
        if len(data['username']) < 2:
            errors.append(['username', "Username must be at least 2 characters in length"])
        if len(data['alios']) < 2:
            errors.append(['alios', "Alios must be at least 2 characters in length"])
        if not re.match(EMAILREG, data['email']):
            errors.append(['email', "Email must be a valid email address"])
        if len(data['password']) < 8:
            errors.append(['password',"Password must be at least eight characters"])
        if not data['password'] == data['confirmpass']:
            errors.append['confirmpass', 'Passwords do not match']
        if errors:
            return [False, errors]
        else:
            current_user = UserDB.objects.filter(email=data['email'])
            for user in current_user:
                print user
            if current_user:
                errors.append(['current_user',"User already exist, please use alternative information"])
                return [False, errors]
            newUser = UserDB(username=data['username'], alios=data['alios'], email=data['email'])
            newUser.hashpw = self.hash_pass(data['password'].encode())
            print newUser.hashpw
            newUser.save()
            return [True, newUser]
    def check_log(self, data):
        errors = []
        current_user = UserDB.objects.filter(email=data['email'])
        if not current_user:
            errors.append(['account',"Email or password incorrect"])
        elif not bcrypt.checkpw(data['password'].encode(),current_user[0].hashpw.encode()):
            errors.append(['account', "Email or password incorrect"])
        if errors:
            return [False, errors]
        else:
            return [Ture, current_user[0]]

class UserDB(models.Model):
    username = models.CharField(max_length=50, blank=False)
    alios = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = userDBManager()
    def __str__(self):
        return self.username + "" + self.alios

class BookDB(models.Model):
    title = models.CharField(max_length=150, blank=False)
    author = models.CharField(max_length=50)
    users = models.ManyToManyField(UserDB, related_name="books")
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class ReviewDB(models.Model):
    book = models.ForeignKey(BookDB)
    User = models.ForeignKey(UserDB)
    review = models.TextField(max_length=200)
    rating = models.IntegerField(min_value=1, max_value=5)
    create_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
