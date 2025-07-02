from django.db import models
import datetime
# Create your models here.


#category of model
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name





class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'





class Product(models.Model):
    name= models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=8)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    discription =models.CharField(max_length=250,blank=True,null=True,default='')
    image = models.ImageField(upload_to='uploads/product/')
    on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=8)
    def __str__(self):
        return  self.name



#customer order
class Order(models.Model):
    prodect = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    address = models.CharField(max_length=200,default='',blank=True)
    phone = models.CharField(max_length=20,default='',blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)


    def __str__(self):
        return  self.product
    


