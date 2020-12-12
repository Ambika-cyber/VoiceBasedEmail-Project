from django import forms

from .models import Mail,User_Detail
from django.contrib.auth.models import User
from django.forms import ModelForm


class MailForm(forms.Form):
    Reciever_Email = forms.EmailField(label_suffix=" ", label= "Reciever Email" ,error_messages={'required':'Enter Reciever Email Address'})
    Subject = forms.CharField(label_suffix=" ",error_messages={'required':'Enter your Subject'}) 
    Message = forms.CharField(label_suffix=" ", widget=forms.Textarea ,error_messages={'required':'Enter Your Message'})
    






