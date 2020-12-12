from django.db import models
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django import forms
from .text_speech import text_to_speech
from django.contrib.auth.models import User
# Registration  models 

        

# Contact form
class Contact_form(models.Model):
    
    Name= models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Contact = models.CharField(max_length=100)
    Message = models.CharField(max_length=100)    
    class Meta:
        db_table = "contact"



class Mail(models.Model):
	to = models.EmailField()
	subject = models.CharField(max_length=280)
	content = models.TextField()
	def __str__(self):
		return self.to 


class UserProfileManager(models.Manager):
    pass

class User_Detail(models.Model):
    Name = models.CharField(max_length=20,null=True)
    gmail_id = models.EmailField(max_length=40, unique=True)
    Age = models.IntegerField(null=True)
    City = models.CharField(max_length=20,null=True)
    State = models.CharField(max_length=20,null=True)
    Country = models.CharField(max_length=20,null=True)
    Phone_Number = models.IntegerField(null=True,  unique=True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    
    
    def __str__(self):
        return self.user.username


