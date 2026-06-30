from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=40)
    email=models.EmailField()
    password=models.CharField(max_length=8)

class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=50)

class Subcategory(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=100)
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    detail = models.TextField()
    price = models.IntegerField()

class Image(models.Model):
    i_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='product_images/')
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    s_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE,null=True,blank=True)

class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    c_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    s_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    Qty = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    o_id = models.IntegerField(null=True, blank=True)

class Order(models.Model):
    o_id=models.AutoField(primary_key=True)
    cart_id=models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    Total=models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Wishlist(models.Model):
    w_id=models.AutoField(primary_key=True)
    s_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Address(models.Model):
    a_id=models.AutoField(primary_key=True)
    Name=models.CharField(max_length=100)
    Address=models.TextField(max_length=200)
    Pincode=models.IntegerField(max_length=6)
    Comments=models.TextField(max_length=500,null=True, blank=True)
    Contact=models.IntegerField(max_length=10)
    state=models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

class Payment(models.Model):
    p_id = models.AutoField(primary_key=True)
    o_id = models.IntegerField()
    Total = models.DecimalField(max_digits=10, decimal_places=2)
    Date = models.DateField()
    Time = models.TimeField()
    Status = models.CharField(max_length=30)
    Type = models.CharField(max_length=30)
    user_id = models.IntegerField()

class Feedback(models.Model):
    f_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField()
    user_id = models.IntegerField()

class ContactUs(models.Model):
    cont_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    comment = models.TextField()