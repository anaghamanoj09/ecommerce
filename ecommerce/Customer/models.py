from django.db import models
from django.contrib.auth.models import User
from Head.models import *
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    Phone=models.CharField(max_length=20)
    Address=models.TextField()
    City=models.CharField(max_length=20)
    State=models.CharField(max_length=20,blank=True,default=0)
    Postal=models.IntegerField(blank=True,default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class cart_tb(models.Model):
    productid=models.ForeignKey(product,on_delete=models.CASCADE)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    count=models.IntegerField()
    price=models.FloatField()

class order_tb(models.Model):
    name=models.CharField(max_length=20)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    zipcode=models.IntegerField()
    email=models.CharField(max_length=20)
    orderdate=models.DateField()
    carrier=models.CharField(max_length=20,null=True,blank=True)
    tracking=models.CharField(max_length=20,null=True,blank=True)
    shippingdate=models.DateField(null=True,blank=True)
    transaction_id=models.CharField(max_length=20,null=True,blank=True)
    paymentdue_date=models.DateField(null=True,blank=True)
    payment_status=models.CharField(max_length=20,default='pending')
    order_status=models.CharField(max_length=20,default="pending")
    order_total=models.FloatField()
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)

class orderitem(models.Model):
    order_id=models.ForeignKey(order_tb,on_delete=models.CASCADE)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    count=models.IntegerField()
    price=models.FloatField()