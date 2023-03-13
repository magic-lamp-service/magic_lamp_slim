from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Image)
admin.site.register(ProductImage)
admin.site.register(AdImage)
admin.site.register(Qa)
admin.site.register(Review)
admin.site.register(Coupon)
