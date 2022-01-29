

# Create your models here.
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import HttpResponse
from django.core.validators import RegexValidator
import datetime
from django import forms





class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class Account(AbstractBaseUser):
    email                     = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                 = models.CharField(max_length=30, unique=True)
    date_joined                = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active                = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    is_premiumuser          = models.BooleanField(default=False)
    ident                   = models.BigIntegerField(validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')] , unique=True , null=True)
    firstname                 = models.CharField(max_length=30, null=True)
    lastname                 = models.CharField(max_length=30, null= True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("The date cannot be in the past!")
    return value

class Vote(models.Model):
    v_name = models.CharField(max_length=100)
    v_code = models.CharField(max_length=100 , primary_key=True)
    v_information = models.CharField(max_length=1000)
    f_date = models.DateField(null=True , auto_now_add=True)#amacımız first date i seçerken bugünün öncesini seçememek
    l_date = models.DateField(null=True , validators=[present_or_future_date])
    who_voted = models.ManyToManyField(Account)


    def __str__(self):
        return self.v_name

    


    


class Candidates(models.Model):
    c_name = models.CharField(max_length=100)
    which_vote = models.ForeignKey(Vote , on_delete=CASCADE)

    def __str__(self):
        return self.c_name

class RegisteredUser(models.Model):
    firstname = models.CharField(max_length=100)

class Stat(models.Model):
    value = models.CharField(max_length=100)
    which_vote = models.CharField(max_length=100)
    l_date = models.CharField(null=True , max_length=25) 
    who_voted = models.CharField(max_length=100 , null=True)

    def __str__(self):
        return self.value