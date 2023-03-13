import os
from telnetlib import STATUS
from django.contrib.auth import SESSION_KEY
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related
import uuid
from ecommerce import settings
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.email


PRODUCT_TYPES = (
    ('retangle', 'retangle'),
    ('square', 'square'),
    ('cylinder', 'cylinder'),
    ('sphere', 'sphere')
)


class Product(models.Model):
    name = models.CharField(max_length=200)
    prog_name = models.CharField(max_length=200, default='lamp')
    price = models.FloatField()
    is_stock  = models.BooleanField(default=True)
    featured_image = models.ImageField(null=True, blank=True, upload_to='products_images')
    short_description = models.TextField(max_length=500, blank=True)
    long_description = models.TextField(max_length=3000, blank=True)
    image_ratio_x = models.IntegerField(default=3, null=True, blank=True)
    image_ratio_y = models.IntegerField(default=2, null=True, blank=True)
    text_spacer_from_top = models.IntegerField(default=85)
    type = models.CharField(
        max_length=20, choices=PRODUCT_TYPES, default='retangle')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products_images')

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        print('URL:', url)
        return url


class AdImage(models.Model):
    image = models.ImageField(upload_to='products_images')
    order = models.IntegerField(default=0)
    show  = models.BooleanField(default=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        print('URL:', url)
        return url


class Review(models.Model):
    text = models.TextField(max_length=1000, blank=False)
    product =  models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer =  models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

class Qa(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=2000)
    order = models.IntegerField(default=0)


COUPON_TYPES = (
    ('per', 'percent'),
    ('sub', 'subtraction'),
)


class Coupon(models.Model):
    code = models.CharField(max_length=8, default=str(uuid.uuid4())[:8])
    discount = models.IntegerField(default=0)
    type = models.CharField(
        max_length=20, choices=COUPON_TYPES, default='per')
    quantity = models.IntegerField(default=100 ,max_length=1000)
    valid =  models.BooleanField(default=True)

    def __str__(self):
        if self.type == 'per':
            return f"{self.discount}% discount"
        if self.type == 'sub':
            return f"-{self.discount} discount"


    def is_valid(code, customer):
        if Coupon.objects.filter(code=code).exists() == False:
            return (False, "Coupon don't exists")
        coupon = Coupon.objects.get(code=code)
        if coupon.valid == False:
            return (False, "Coupon is not valid")
        if len(Order.objects.filter(customer=customer, coupon=coupon, complete=True)) > 0:
            return (False, "You already used that coupon")
        return (True, None)

    def update_quantity(self, coupon):
        coupon.quantity = coupon.quantity - 1
        if coupon.quantity == 0:
            coupon.valid = False
        coupon.save()

    def get_discount_price(self, original_price):
        if self.type == 'per':
            return "%.2f" % (original_price * (100 - self.discount) * 0.01)
        if self.type == 'sub':
            return original_price - self.discount
    
    def get_discount_drop(self, price):
            if self.type == 'per':
                return "%.2f" % (self.discount * 0.01 * price)
            if self.coupon.type == 'sub':
                return "%.2f" % (price - self.discount)
            

STATUSES = (
    ('no_pay', 'לא שולם'),
    ('preparation', 'בהכנת ההזמנה'),
    ('ready', 'מוכן לשליחה'),
    ('shipped', 'נשלח'),
    ('Finished', 'הזמנה סגורה')
)   


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(
        max_length=20, choices=STATUSES, default='no_pay')
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def shipping(self):
        return True
    
    @property
    def get_shipping(self):
        shipping_address = self.shipping.first()
        return shipping_address

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        if self.coupon:
            total = self.coupon.get_discount_price(total)
        return total

    @property
    def get_original_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_order_items(self):
        orders_items = OrderItem.objects.filter(order=self)
        return orders_items

    @property
    def get_discount_drop(self):
        if Coupon:
            if self.coupon.type == 'per':
                return "%.2f" % (self.coupon.discount * 0.01 * self.get_original_cart_total)
            if self.coupon.type == 'sub':
                return "%.2f" % (self.get_original_cart_total - self.coupon.discount)

class Image(models.Model):
    file = models.ImageField(upload_to='customers_images', null=True, blank=True)
    image_id = models.CharField(max_length=200, default="")
    fb_link = models.URLField(default="", null=True, blank=True)
    is_text = models.BooleanField(default=False)
    text = models.CharField(max_length=50, default="", null=True, blank=True)
    text_size = models.IntegerField(default=30, null=True, blank=True)
    text_font = models.CharField(max_length=20, default="sans-serif", null=True, blank=True)
    text_color = models.CharField(max_length=20, default="#000000", null=True, blank=True)
    is_resized = models.BooleanField(default=False)

    def __str__(self):
        return str(self.image_id)

    def remove(self):
        try:
            os.remove(self.file.path)
            self.file = None
            super().save()
        except:
            print("Something went wrong")

    @property
    def imageURL(self):
        try:
            url = self.fb_link
        except:
            url = ''
        print('URL:', url)
        return url

    @property
    def image_localURL(self):
        try:
            url = self.file.url
        except:
            url = ''
        print('URL:', url)
        return url

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_image(self):
        return Image.objects.get(image_id=self.image_id)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


SHIPPING_TYPES = (
    ('self_pickup', 'Self-pickup'),
    ('home_delivery', 'Home-delivery'),
    ('distribution_point', 'Delivery to distribution point'),
)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    shipping_type =  models.CharField(
        max_length=100, choices=SHIPPING_TYPES, default='self_pickup')