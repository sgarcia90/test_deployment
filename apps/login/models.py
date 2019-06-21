from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import bcrypt
import re


class UserManager(models.Manager):
    def user_validator(self, post_data):
        first_name = post_data['f_name']
        last_name = post_data['l_name']
        email = post_data['email']
        password = post_data['password']
        confirm_pw = post_data['confirm_pw']
        date_of_birth = datetime.strptime(post_data['date_of_birth'], '%Y-%m-%d').date()
        today = date.today()
        age_check = today.replace(year=today.year-13)

        email_check = User.objects.filter(email=email)
        errors = {}

        if not re.match(r"^[A-Za-z]{2,45}$", first_name):
            errors['first_name'] = "Please enter a first name that is at least 2 characters long."
        if not re.match(r"^[A-Za-z]{2,45}$", last_name):
            errors['last_name'] = "Please enter a first name that is at least 2 characters long."
        if date_of_birth > age_check:
            errors['age_check'] = "You must be at least 13 years old."
        if not re.match(r"^[^@]+@[^@]+\.[^@]{2,4}$", email):
            errors['email'] = "Please enter a valid email address."
        if email_check:
            errors['email'] = "That email has already been used."
        if password != confirm_pw:
            errors['password'] = "Please make sure your passwords match."
        return errors

    def user_login(self, post_data):
        email = post_data['email']
        password = post_data['password']
        user_filter = User.objects.filter(email=email)

        errors = {}

        if len(user_filter) > 0:
            user = user_filter[0]
        else:
            errors['failed'] = "Either the email or password entered was incorrect."
            return errors
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            errors['failed'] = "Either the email or password entered was incorrect."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=90)
    date_birth = models.DateField()
    password = models.CharField(max_length=255)
    objects = UserManager()
