from django.urls import path,include
from Common import views
urlpatterns = [
    path('',views.login_pg,name='login_pg'),
    path('login_user',views.login_user,name='login_user'),
    path('register',views.register,name='register'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('reset_password/<uidb64>/<token>/',views.reset_password,name='reset_password')
]
