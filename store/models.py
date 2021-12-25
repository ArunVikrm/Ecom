from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=30,null=True)
    email = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30,null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def shipping(self):
        shipping = False
        cartItems = self.cartitem_set.all()
        for i in cartItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        cartitems = self.cartitem_set.all()
        #total = sum([item.get_total for item in cartitems])
        return 55
    
    def get_cart_items(self):
        cartitems = self.cartitem_set.all()
        total = sum([item.quantity for item in cartitems])
        return total

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
