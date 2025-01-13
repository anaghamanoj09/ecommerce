from django.shortcuts import render,redirect                                          
from Head.models import *
from Customer.models import *
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.urls import reverse
from django.core.mail import send_mail
# uname:admin123 passwd:admin#123

def login_pg(request):
    return render(request,'common/login.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None and user.groups.filter(name="Customer").exists():
            login(request,user)
            return redirect('customer_home')
        elif user is not None and user.is_superuser:
            login(request,user)
            return render(request,'Head/homepg.html') 
        else:
            messages.add_message(request,messages.INFO,"error")
    return render(request,'Common/login.html')

def register(request):
    if request.method == 'POST':
        print("hi")
        fname=request.POST['fname']
        lname=request.POST['lname']
        uname=request.POST['uname']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        password=request.POST['password']
        email=request.POST['email']
        repeat=request.POST['repeat']
        if password == repeat:
            if User.objects.filter(username=uname).exists():
                messages.error(request,"Username already exist")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=uname,password=password,email=email)
                user.save()
                customer=Customer.objects.create(user=user,Phone=phone,Address=address,City=city)
                customer.save()
                group,craete=Group.objects.get_or_create(name="Customer")
                user.groups.add(group)
                messages.add_message(request,messages.INFO,"Registration successfull")
                return redirect(login_user)
    return render(request,'Common/register.html')

def forgot_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        try:
            user=User.objects.get(email=email)
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            reset_link=request.build_absolute_uri(reverse('reset_password',args=[uid,token]))
            send_mail(
                'Reset your password',
                f'Click the link below to reset your password:\n\n{reset_link}',
                'p33080204@gmail.com',
                [email],
                fail_silently=False,
            )
            messages.success(request,'Password reset link sent to your email')
        except User.DoesNotExist:
            messages.error(request,'No User found with this email')
    return render(request,'Common/forgot_password.html')

def reset_password(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(User.DoesNotExist,ValueError,TypeError,OverflowError):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        if request.method =='POST':
            newpsswd=request.POST.get('new')
            confirmpsswd=request.POST.get('confirm')
            user.set_password(newpsswd)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect(login_pg)
        return render(request,'Common/reset_password.html')
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect(forgot_password)