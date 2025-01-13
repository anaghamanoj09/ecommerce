from django.db import models
class header(models.Model):
    username=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

class category(models.Model):
    c_name=models.CharField(max_length=20)

class material(models.Model):
    material_type=models.CharField(max_length=20)

class product(models.Model):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=20)
    listprice=models.IntegerField()
    price=models.IntegerField()
    price50=models.IntegerField()
    price100=models.IntegerField()
    category=models.ForeignKey(category,on_delete=models.CASCADE)
    materialtype=models.ForeignKey(material,on_delete=models.CASCADE)
    image=models.ImageField()
