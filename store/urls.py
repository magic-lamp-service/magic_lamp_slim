from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('product/<slug>', views.product, name='product'),
	path('image_cropper/<slug>', views.image_cropper, name='image_cropper'),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('order_complete/', views.order_complete, name="order_complete"),

	path('remove_background/', views.remove_background, name='remove_background'),
	path('moon_lamp_editor/<slug>', views.moon_lamp_editor, name='moon_lamp_editor'),
    
	path('about_us', views.about_us, name="about_us"),
	path('our_product', views.product_info, name="our_product"),

	path('login/', views.login, name="login"),
	path('logout/', views.logout, name="logout"),
	path('register/', views.register, name="register"),
	path('user_orders/', views.user_orders, name="user_orders"),
	path('user_info/', views.user_info, name="user_info"),

	path('admin_orders/', views.admin_orders.as_view(), name="admin_orders"),
	path('order_details/<int:pk>', views.order_details.as_view(), name="order_details"),

	path('update_item/', views.updateItem, name="update_item"),
	path('update_image/', views.update_image, name="update_image"),
	path('process_order/', views.processOrder, name="process_order"),
	path('is_coupon_valid/', views.is_coupon_valid, name="is_coupon_valid"),

]