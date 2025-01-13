from django.shortcuts import render,redirect
from Head.models import *
from django.contrib import messages
from django.contrib.auth import logout
from Customer.models import *
from django.http import JsonResponse
import datetime
from django.core.paginator import Paginator


def home(request):
    return render(request,'Head/homepg.html')

def head_logout(request):
    logout(request)
    return redirect('login_pg')

def category_list(request):
    user=category.objects.all()
    paginator=Paginator(user,3)
    page_number=request.GET.get('page',1)
    page_obj=paginator.get_page(page_number)
    return render(request,'Head/category_list.html',{'page_obj':page_obj})

def create_category(request):
    return redirect(add_category)

def add_category(request):
    if request.method == 'POST':
        name=request.POST['category']
        data=category(c_name=name)
        data.save()
        return redirect(category_list)
    return render(request,'Head/add_category.html')

def edit_category(request,id):
    user=category.objects.filter(id=id)
    return render(request,'Head/edit_category.html',{'us':user})

def editAction(request):
    id=request.POST['id']
    name=request.POST['category']
    category.objects.filter(id=id).update(c_name=name)
    return redirect(category_list)

def delete_category(request,id):
    category.objects.filter(id=id).delete()
    messages.add_message(request,messages.INFO,"Deleted")
    return redirect(category_list)

def material_create(request):
    return render(request,'Head/add_material.html')

def material_list(request):
    user=material.objects.all()
    paginator=Paginator(user,3)
    page_number=request.GET.get('page,1')
    page_obj=paginator.get_page(page_number)
    return render(request,'Head/material_list.html',{'page_obj':page_obj})

def add_material(request):
    if request.method == 'POST':
        mtype=request.POST['material']
        data=material(material_type=mtype)
        data.save()
        return redirect (material_list)
    return render(request,'Head/add_material.html')

def update_material(request,id):
    user=material.objects.filter(id=id)
    return render(request,'Head/update_material.html',{'us':user})

def updateAction(request):
    id=request.POST['id']
    mtype=request.POST['material']
    material.objects.filter(id=id).update(material_type=mtype)
    return redirect(material_list)

def delete_material(request,id):
    material.objects.filter(id=id).delete()
    messages.add_message(request,messages.INFO,"Deleted")
    return redirect(material_list)

def product_list(request):
    user=product.objects.all()
    paginator=Paginator(user,1)
    page_number=request.GET.get('page',1)
    page_obj=paginator.get_page(page_number)
    return render(request,'Head/product_list.html',{'page_obj':page_obj})

def create_product(request):
    if request.method == 'POST':
        name=request.POST['name']
        descr=request.POST['description']
        listp=request.POST['lprice']
        price=request.POST['price']
        price1=request.POST['price50']
        price2=request.POST['price100']
        ctgry=request.POST['category']
        mtype=request.POST['materialtype']
        image=request.FILES['image']
        user=product(name=name,description=descr,listprice=listp,price=price,price50=price1,price100=price2,category_id=ctgry,materialtype_id=mtype,image=image)
        user.save()
        return redirect(product_list)
    data=category.objects.all()
    data1=material.objects.all()
    return render(request,'Head/create_product.html',{'da':data,'ua':data1})

def update_product(request,id):
    user=product.objects.filter(id=id)
    data=category.objects.all()
    data1=material.objects.all()
    return render(request,'Head/update_product.html',{'us':user,'da':data,'ua':data1})

def updateAction_product(request):
    id=request.POST['id']
    name=request.POST['name']
    oldimg=product.objects.get(id=id)
    if len(request.FILES)>0:
        img=request.FILES['image']
    else:
        img=oldimg.image

    descr=request.POST['description']
    listp=request.POST['lprice']
    price=request.POST['price']
    price1=request.POST['price50']
    price2=request.POST['price100']
    ctgry=request.POST['category']
    mtype=request.POST['materialtype']
    oldimg.image=img
    oldimg.save()
    product.objects.filter(id=id).update(name=name,description=descr,listprice=listp,price=price,price50=price1,price100=price2,category_id=ctgry,materialtype_id=mtype)
    return redirect(product_list)

def back_list(request):
    return redirect(product_list)

def delete_product(request,id):
    product.objects.filter(id=id).delete()
    return redirect(product_list)

def manage_order(request):
    user=order_tb.objects.all()
    paginator=Paginator(user,3)
    page_number=request.GET.get('page',1)
    page_obj=paginator.get_page(page_number)
    return render(request,'Head/manage_order.html',{'page_obj':page_obj})

def order_details(request):
    order = request.GET.get('detail', 'all') 
    print(f"Order filter: {order}")  
    if order == "all":
        d = order_tb.objects.all().order_by('id')  
    elif order == "process":
        d = order_tb.objects.filter(order_status="Processing").order_by('id')
    elif order == "pending":
        d = order_tb.objects.filter(payment_status="pending").order_by('id')
    elif order == "completed":
        d = order_tb.objects.filter(payment_status="completed").order_by('id')
    else:
        d = order_tb.objects.filter(order_status="Rejected").order_by('id')

    paginator = Paginator(d, 3)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        print(f"Pagination error: {e}")  
        page_obj = paginator.get_page(1) 
    return render(request, 'Head/order_details.html', {'page_obj': page_obj, 'order': order})

def pickup_details(request,id):
    data=order_tb.objects.filter(id=id)
    user=orderitem.objects.filter(order_id_id=id)
    t=[]
    for i in user:
        total=i.count*i.price
        t.append(total)
    return render(request,'Head/pickup_details.html',{'da':data,'us':user,'t':t})

def start_processing(request,id):
    status="Processing"
    data=order_tb.objects.filter(id=id).update(order_status=status)
    return redirect(manage_order)

def ship_order(request):
    id=request.POST['id']
    c=request.POST['carrier']
    track=request.POST['tracking']
    ship_date=datetime.date.today()
    orderstatus="completed"
    order_tb.objects.filter(id=id).update(carrier=c,tracking=track,shippingdate=ship_date,order_status=orderstatus,)
    return redirect(manage_order)

def cancel_order(request,id):
    status="Rejected"
    order_tb.objects.filter(id=id).update(order_status=status)
    return redirect(manage_order)

def reset_psswd(request):
    if request.method == 'POST':
        id=request.user.id
        print(id)
        data=User.objects.get(id=id)
        old=request.POST['oldpsswd']
        new=request.POST['newpsswd']
        confirm=request.POST['confirmpsswd']
        if data.check_password(old):
            if new == confirm:
                data.set_password(new)
                data.save()
                return render(request,'Head/homepg.html')
            else:
                messages.add_message(request,messages.INFO,"Enter new password")
                return redirect(reset_psswd)
        else:
            messages.add_message(request,messages.INFO,"wrong password")
            return render(request,'Head/reset_psswd.html')
    return render(request,'Head/reset_psswd.html')