from django.shortcuts import render,redirect,get_object_or_404
from Head.models import *
from Customer.models import *
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views import View
from django.urls import reverse
from datetime import date


stripe.api_key = settings.STRIPE_SECRET_KEY



def customer_home(request):
    user=product.objects.all()
    return render(request,'Customer/customer_home.html',{'us':user})

def customer_logout(request):
    logout(request)
    return redirect('login_pg')

def product_details(request,id):
    user=product.objects.filter(id=id)
    return render(request,'Customer/product_details.html',{'us':user})

def add_tocart(request,id):
    if request.method == 'POST':
        cou=request.POST['count']
        count=int(cou)
        user=product.objects.filter(id=id)
        if count<50:
            price=user[0].price
        elif count<100:
            price=user[0].price50
        else:
            price=user[0].price100
        user_id=request.user.id
        data=cart_tb(count=count,productid_id=id,price=price,userid_id=user_id)
        data.save()
        return redirect(customer_home)
    return render(request,'Customer/product_details.html')

def view_cart(request):
    userid=request.user.id
    cart=cart_tb.objects.filter(userid_id=userid)
    gt=0
    for i in cart:
        total=i.count*i.price
        gt=gt+total
    request.session['gt']=gt
    return render(request,'Customer/view_cart.html',{'us':cart,'g':gt})

def less_quantity(request,id):
    user=cart_tb.objects.filter(id=id)
    count=user[0].count
    quantity=count-1
    user.update(count=quantity)
    return redirect(view_cart)

def add_count(request,id):
    data=cart_tb.objects.filter(id=id)
    count=data[0].count
    quantity=count+1
    data.update(count=quantity)
    return redirect(view_cart)

def delete_cart(request,id):
    cart_tb.objects.filter(id=id).delete()
    return redirect(view_cart)

def summary(request):
    userid=request.user.id
    total=request.session['gt']
    data=Customer.objects.filter(user_id=userid)
    user=cart_tb.objects.filter(userid_id=userid)
    today = date.today()
    new_date = today + timedelta(days=10)
    return render(request,'Customer/summary.html',{'da':data,'us':user,'total':total,'new_date': new_date})

class SuccessView(View):
    def get(self, request):
        session_id=request.GET.get('session_id')
        if not session_id:
            return render(request,'Customer/succes.html',{'error':'Session id missing'})
        try:
            session=stripe.checkout.Session.retrieve(session_id)
            order_id=session.metadata.get('order_id')
            print(order_id)
            if not order_id:
                return render(request,'Customer/success.html',{'error':'order id not found'})
            order=order_tb.objects.get(id=order_id)
            if session.payment_status == "paid":
                print("hi")
                order.order_status="pending"
                order.transaction_id=session_id
                order.paymentdue_date=date.today()
                order.payment_status="completed"
                order.save()
                return render(request,'Customer/success.html',{
                    'order':order,
                    'payment_status':session.payment_status,
                    'order_status': order.order_status,
                    'transaction_id':order.transaction_id,
                    'paymentdue_date':order.paymentdue_date,
                    'payment_status':order.payment_status,
                })
        except stripe.error.StripeError as e:
            return render(request, 'Customer/success.html', {'error': str(e)})
        return render(request, 'Customer/success.html')  # Success page

class CancelledView(View):
    def get(self, request):
        return render(request, 'Customer/cancelled.html')  # Cancelled page

def place_order(request):
    if request.method == 'POST':
        user=get_object_or_404(User,id=request.user.id)
        userid=request.user.id
        email=user.email
        name=request.POST['name']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        post=request.POST['post']
        total=request.session['gt']
        dates=date.today()
        data=order_tb(name=name,phone=phone,address=address,city=city,zipcode=post,email=email,orderdate=dates,order_total=total,user_id_id=userid)
        data.save()

        item=cart_tb.objects.filter(userid_id=userid)
        for i in item:
            quantity=i.count
            price=i.price
            orderid=data.id
            productid=i.productid.id
            newdata=orderitem(count=quantity,price=price,order_id_id=orderid,product_id_id=productid)
            newdata.save()
            order_items=cart_tb.objects.filter(userid_id=userid)
            payment_method_types=['card'],
            line_items = []
            for item in order_items:
                    line_items.append({
                        'price_data':{
                            'currency':'usd',
                            'product_data':{
                                'name':item.productid.name,
                            },
                            'unit_amount':int(item.price * 100),
                        },
                        'quantity':item.count,
                        })
                    

                    domain_url = 'http://127.0.0.1:8000/' 
            try:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                success_url=request.build_absolute_uri(reverse('success')) +"?session_id={CHECKOUT_SESSION_ID}",  # Dynamic session_id
                cancel_url=domain_url + 'cancelled/',
                metadata={
                    'order_id':orderid}
            
                )
            except Exception as e:
                return JsonResponse({'error': str(e)})

        return redirect(checkout_session.url)
    return render(request, 'Customer/summary.html')  

def order_manage(request):
    userid=request.user.id
    user=order_tb.objects.filter(user_id_id=userid)
    return render(request,'Customer/order_manage.html',{'us':user})

def details(request):
    userid=request.user.id
    d=request.GET['detail']   
    if d == "process":
        user=order_tb.objects.filter(user_id=userid,order_status="Processing")
    elif d == "all":
        user=order_tb.objects.filter(user_id_id=userid)
    elif d == "pending":
        user=order_tb.objects.filter(user_id_id=userid,order_status="pending")
    elif d == "completed":
        user=order_tb.objects.filter(user_id_id=userid,order_status="completed")
    else:
        user=order_tb.objects.filter(user_id_id=userid,order_status="Rejected")
    return render(request,'Customer/details.html',{'us':user})

def status_details(request,id):
    data=order_tb.objects.filter(id=id)
    user=orderitem.objects.filter(order_id_id=id)
    t=[]
    for i in user:
        total=i.count*i.price
        t.append(total)
    return render(request,'Customer/status_details.html',{'da':data,'us':user,'t':t})

def cancel(request,id):
    status="Rejected"
    order_tb.objects.filter(id=id).update(order_status=status)
    return redirect(order_manage)

def change_psswd(request):
    if request.method == 'POST':
        userid=request.user.id
        print(userid)
        user=User.objects.get(id=userid)
        oldpsswd=request.POST['old']
        newpsswd=request.POST['new']
        confirmpsswd=request.POST['confirm']
        if user.check_password(oldpsswd):
            if(newpsswd==confirmpsswd):
                user.set_password(newpsswd)
                user.save()
                return render(request,'Customer/customer_home.html')
            else:
                messages.add_message(request,messages.INFO,"Enter new password")
                return redirect(change_psswd)
        else:
            messages.add_message(request,messages.INFO,"wrong password")
            return render(request,'Customer/change_psswd.html')
    return render(request,'Customer/change_psswd.html')

def my_account(request):
    user=request.user
    customer=get_object_or_404(Customer,user=user)
    if request.method == 'POST':
        user.first_name=request.POST['name']
        user.username=request.POST['username']
        user.email=request.POST['email']
        user.save()
        customer.Phone=request.POST['phone']
        customer.Address=request.POST['address']
        customer.City=request.POST['city']
        customer.Postal=request.POST['post']
        customer.save()
        messages.add_message(request,messages.INFO,"Updated")
        return redirect(my_account)
    return render(request,'Customer/my_account.html',{'user':user,'customer':customer})
