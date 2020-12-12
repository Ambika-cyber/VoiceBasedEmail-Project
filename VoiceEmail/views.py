from django.shortcuts import render, redirect # django pacakge and showrtcuts module
from django.http import HttpResponse
from sqlite3 import connect
from .models import Contact_form, User_Detail
import mysql.connector
from operator import itemgetter
from  django.contrib import messages
from . text_speech import text_to_speech
import pyttsx3
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .forms import MailForm
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth.forms import SetPasswordForm
import nest_asyncio




def home_view(request):
    return render(request, 'home.html',{'titles':'Voice Based Email','link':'http://127.0.0.1:8000/'})


def terms(request):
    return render(request,'terms.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    if request.method == "POST":
        user = Contact_form()
        user.Name = request.POST.get('name')
        user.Email = request.POST.get('email')
        user.Contact = request.POST.get('contact')
        user.Message = request.POST.get('message')
      
        if( user.Name ==' ' or user.Email == ' ' or user.Contact == ' ' or user.Message == ' '):
            text_to_speech("All fields are required")
            messages.error(request, "All fields are required")    
            return redirect('contact')
        else:
            user.save()
            text_to_speech("Your information send successfully. We will contact to you soon.")
            messages.info(request, "Your information send successfully. We will contact to you soon.")
            
    return render(request,'contact.html')   

def text(request):
    value = request.GET['name']
    obj = pyttsx3.init()
    obj.say(value)
    obj.runAndWait()
    return redirect('/')


def login_view(request):
    print("i m here")
    if not request.user.is_authenticated:
        print("auth")
        if request.method == "POST":
            print("post")
            # if user exist and
            uname = request.POST.get('username')
            pwd = request.POST.get('password')
            #creae user object
            user = auth.authenticate(username = uname, password = pwd)
            if user is not None:
                print("none")
                auth.login(request, user)
                text_to_speech("login successful")
                return HttpResponseRedirect('/vmail/')
            else:
                print("wrong")
                try:
                    text_to_speech("username and password is wrong")
                except:
                    return render(request,'login.html', {'error':"invalid login"})     
        else:
            print("login")
            return render(request,'login.html')    
    else:
        print("out 1")
        return render(request,'login.html')
    print("out")
    return render(request,'login.html')


def register_view(request):
    context = {}
    if request.method == "POST":
            if request.POST['password'] == request.POST['Cpass']:
                print("pass same")
                try:
                    user = User.objects.get(username=request.POST.get('username'))
                    return render(request, 'register.html', {'error':'username has already been taken'})
                except User.DoesNotExist:
                    conn = connect(database = "db.sqlite3")
                    cursor1 = conn.cursor()
                    sqlcommand1 = "select gmail_id from VoiceEmail_user_detail"
                    cursor1.execute(sqlcommand1)
                    gmail_list = []
                    for i in cursor1:
                        gmail_list.append(i)
                    gmail_ids = list(map(itemgetter(0),gmail_list)) 
                    print(gmail_ids) 
                    sqlcommand1 = "select Phone_Number from VoiceEmail_user_detail"
                    cursor1.execute(sqlcommand1)
                    Phone_list = []
                    for i in cursor1:
                        Phone_list.append(i)
                    phone_no = list(map(itemgetter(0),Phone_list)) 
                    print(phone_no) 
                
                    name    = request.POST.get('fname')
                    gmailid = request.POST.get('gmailid')
                    age = request.POST.get('Age')
                    city = request.POST.get('City')
                    state = request.POST.get('State')
                    country = request.POST.get('Country')
                    phone = request.POST.get('Phone')
                    print(gmailid)
                    phn = int(phone)
                    age = int(age)
                    length = len(phone)
                    if(length==10 and age>=18 ):
                
                        for i in range(0,len(gmail_ids)):
                            if(gmail_ids[i]==gmailid):
                                text_to_speech("Your email already registered . Please login yourself")
                                messages.info(request,"This email already registered . Please login yourself.")
                                return  render(request, 'register.html')
                            
                        for i in range(0,len(phone_no)):
                            if(phone_no[i]==phn):
                                text_to_speech("Your Phone Number already registered. PLease login Yourself.")
                                messages.info(request,"Phone Number already registered. PLease login Yourself.")
                                return render(request, 'register.html')
                        try:
                            user1 = User.objects.create_user(username = request.POST.get('username'), password = request.POST.get('password'))
                            user1.save()
                            newexuser = User_Detail(user=user1,Name = name,gmail_id=gmailid,Age=age,City=city, State=state, Country=country, Phone_Number=phone)
                            print(newexuser)                           
                            newexuser.save()
                            messages.info(request, "Registration successful")
                            text_to_speech("Registration successful")
                        except :     
                            text_to_speech("Error Phone number and Email Id must be unique")     
                            return render(request,'register.html',{'error':"Phone number and Email Id must be unique"})
                    elif(age<18):
                        text_to_speech("Your age is not 18 and above , You are not allowed to use this website.")
                        return render(request, 'home.html')
                    elif(phn!=10):
                        messages.info(request,"Please enter 10 digit valid phone number")
                        text_to_speech("Please enter 10 digit valid phone number and your age must be 18 years old and above.")
                        return render(request, 'register.html')
            else:
                text_to_speech("password and confirm password is not same")
                return render(request, 'register.html', {'error':'Passwords dont match'}) 
    else:
        return render(request,'register.html') 
    return render(request,'register.html')   

@login_required(login_url='/vlogin/')
def view_profile(request):
    user = request.user
    data = User_Detail.objects.filter(user=request.user)
    text_to_speech("Welcome to profile page")
    return render(request,'profile.html',{'d':data,'user':user})



@login_required(login_url='/vlogin/')
def edit_profile(request):
    context = {}
    data = User_Detail.objects.get(user_id = request.user.id)
    context['data'] = data
    if request.method == "POST":
        name    = request.POST.get('fname')
        gmailid = request.POST.get('gmailid')
        city = request.POST.get('City')
        state = request.POST.get('State')
        country = request.POST.get('Country')
        phone = request.POST.get('Phone')
        length = len(phone)
        
        if(length==10):
            data.Name = name
            data.gmail_id = gmailid
            data.City = city
            data.State = state
            data.Country = country
            data.Phone_Number = phone
            data.save()
            context["status"] = "Profile Updated Successfully"
            text_to_speech("Profile Updated Successfully")
        
        else:
            context["status"] = "Please enter valid 10 digit phone number"
        
        
    return render(request,'edit_profile.html',context)

def vlogout(request):
   auth.logout(request)
   text_to_speech("logout successfully")
   return HttpResponseRedirect('/vlogin/')


def forgot_password(request):
        if request.method == "POST":
            uname = request.POST.get('Username') 
            pwd = request.POST.get('Password') 
            
            conn = connect(database = "db.sqlite3")
            cursor1 = conn.cursor()
            sqlcommand1 = "select username from auth_user"
            cursor1.execute(sqlcommand1)
            e = []
            for i in cursor1:
                e.append(i)
            res1 = list(map(itemgetter(0),e)) 
            print(res1)   
            k=len(res1)
            for i in range(0, k):
                count =0
                if res1[i]== uname:    
                    u = User.objects.get(username= uname)
                    u.set_password(pwd)
                    u.save()
                    text_to_speech("password changed successfully")
                    return render(request, 'forgotpass.html', {'message':'Password changed successfully'})
            
            text_to_speech("username is invalid")
            return render(request, 'forgotpass.html', {'message':'Username is invalid'})
        else:
            return render(request, 'forgotpass.html')




@login_required(login_url='/vlogin/')
def vmail_create(request):
    if request.method == 'POST':
            subject = request.POST.get('Subject')
           
            from_email = request.POST.get('Reciever_Email')
            print(from_email)
            message = request.POST.get('Message')
            print(message)
            user = request.user
            data = User_Detail.objects.filter(user=request.user)
            for i in data:
                sender = i.gmail_id
                name = i.Name
            
            sub = "\n<-----I am sending mail using Voice based email website---->\n" 
            name = "My name is "+name+"\n"
            gmail = "My gmail Id :"+ sender +"\nMessage:"
            msg = name+ gmail + message + sub# accessing the subject value enter by user, here 'Subject' is a key of dict.
            sender_mail = "mvoice064@gmail.com"
            try:
                try:
                    send_mail(subject, msg,sender_mail, [from_email])
                    text_to_speech("Mail Send successfully")
                    messages.info(request, "Mail send successfully")
                except:
                    text_to_speech("Internet connection Error ,Please connect to the internet")
                    messages.error(request,"Internet connection Error ")
                    return HttpResponseRedirect('/vmail/')
            
            except BadHeaderError:
                return HttpRespornse('Invalid header found.')
    else:
        return render(request, "vmail_send.html")
    return HttpResponseRedirect('/vmail/')




def admin_login(request):
    return redirect('admin/')

@login_required(login_url='/vlogin/')
def delete_profile(request):
    if request.method == "POST":
        id = User_Detail.objects.get(user_id = request.user.id)
        id.delete()
        pid = User.objects.get(pk=request.user.id)
        pid.delete()
        text_to_speech(" Your Profile Deleted Successfully")
        return HttpResponseRedirect('/vlogin/')
    else:
        return render(request,"delete_profile.html")