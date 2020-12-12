from django.urls import path, include
from . import views # imprt from current pacakage

urlpatterns = [
    path('', views.home_view),  # url defimes for Home Page http://127.0.0.1:8000/vmail/
    path('text_speech/',views.text, name = 'text'),
    path('vsignup/',  views.register_view, name= 'vsignup'),
    path('vlogin/', views.login_view, name = 'vlogin'), # object of myview
    path('about/', views.about_view, name = 'about'),
    path('contact/', views.contact_view, name = 'contact'),
    path('vlogout/', views.vlogout, name = 'vlogout'),
    path('forgotpass/', views.forgot_password, name = 'forgotPass'),
    path('admin/',views.admin_login,name= 'admin'),
    path('profile/',views.view_profile,name= 'profile'),
    path('vmail/',views.vmail_create,name= 'vmail'),
    path('edit/',views.edit_profile,name= 'edit'),
    path('del/',views.delete_profile,name = 'del'),
    path('terms/',views.terms,name = 'terms'),
]