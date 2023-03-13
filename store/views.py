from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.forms.models import model_to_dict

import json
import datetime

from .utils import cartData, guestOrder
from .forms import *
from .models import *
from .decorators import *
from .extras import send_email

def remove_background(request):
	data = cartData(request)
	cartItems = data['cartItems']
	print(data)
	
	product = Product.objects.get(prog_name='moon_lamp')
	form = ImageForm()

	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			return JsonResponse('image added', safe=False)
		else:
			messages.error(request, 'something went wrong: ' + str(form.errors))

	context = {'cartItems': cartItems, 'form': form, 'product': product, 'moon_background': Image.objects.get(image_id='moon_background')}
	return render(request, 'store/remove_background.html', context)

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	print(data)

	products = Product.objects.all()
	ad_images = AdImage.objects.filter(show=True).order_by('order')

	context = {'products': products, 'cartItems': cartItems, 'adImages': ad_images}
	return render(request, 'store/store.html', context)

def about_us(request):
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'cartItems': cartItems}
	return render(request, 'information/about_us.html', context)

def product_info(request):
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'cartItems': cartItems}
	return render(request, 'information/product_info.html', context)

def product(request, slug):
	data = cartData(request)
	cartItems = data['cartItems']
	print(data)
	print(slug)

	product_name = slug
	product = Product.objects.filter(name=product_name)[0]
	qas = Qa.objects.order_by('order')
	reviews = Review.objects.filter(product=product)
	form = ReviewForm()
	if request.method == 'POST' and request.user.is_authenticated:
		form = ReviewForm(request.POST, request.FILES)
		if form.is_valid():
			review = form.save()
			review.product = product
			review.customer = Customer.objects.get(user=request.user)
			review.save()
			messages.success(request, 'your review is added')
			return redirect(request.path)
		else:
			messages.error(request, 'something went wrong')

	context = {'product': product, 'cartItems': cartItems, 'qas': qas, 'form': form, 'reviews': reviews}
	return render(request, 'store/product.html', context)

def moon_lamp_editor(request, slug):
	data = cartData(request)
	cartItems = data['cartItems']

	img_id= slug
	product = Product.objects.get(prog_name='moon_lamp')
	original_img = Image.objects.get(image_id=img_id)
	form = ImageForm()
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)

		if form.is_valid():
			original_img.text = form.cleaned_data.get('text')
			original_img.is_text = form.cleaned_data.get('is_text')
			original_img.font = form.cleaned_data.get('font')
			original_img.fb_link = form.cleaned_data.get('fb_link')
			original_img.remove()

			original_img.save()
			return JsonResponse('Item was added', safe=False)
		else:
			print('error while save image: ' + str(form.errors))
			messages.error(request, 'something went wrong...')

	context = {'cartItems': cartItems, 'form': form, 'product': product}
	context['img'] = original_img
		
	return render(request, 'store/moon_lamp_editor.html', context)

def image_cropper(request, slug):
	data = cartData(request)
	cartItems = data['cartItems']
	product_id = slug

	product = Product.objects.get(pk=product_id)

	form = ImageForm()
	if request.method == 'POST':		
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			image = form.save()
			messages.success(request, 'image is uploaded')
		else:
			print('error while save image: ' + str(form.errors))
			messages.error(request, form.errors)

	context = {'cartItems': cartItems, 'form': form, 'product': product}
		
	return render(request, 'store/image_cropper.html', context)


def login(request):
	if request.user.is_authenticated:
		return redirect('store')

	data = cartData(request)
	cartItems = data['cartItems']
	context = {'cartItems': cartItems}

	if request.method == 'POST':
		user_name = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=user_name, password=password)

		if user is not None:
			login_user(request, user)
			return redirect('store')
		else:
			messages.error(request, 'Username OR password is incorrect')
	return render(request, 'user/login.html', context)

login_required(login_url='store')
def user_orders(request):
	data = cartData(request)
	cartItems = data['cartItems']
	customer = Customer.objects.get(user=request.user)
	orders = Order.objects.filter(customer=customer)
	context = {'cartItems': cartItems, "orders": orders}

	return render(request, 'user/user_orders.html', context)

login_required(login_url='store')
def user_info(request):
	if not request.user.is_authenticated:
		return redirect('store')

	data = cartData(request)
	cartItems = data['cartItems']
	customer = Customer.objects.get(user=request.user)
	context = {'cartItems': cartItems, "customer": customer}

	return render(request, 'user/user_info.html', context,)

login_required(login_url='store')
def logout(request):
	logout_user(request)
	return redirect('login')


def register(request):
	if request.user.is_authenticated:
		return redirect('store')

	data = cartData(request)
	cartItems = data['cartItems']

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			Customer.objects.create(user=user, name=user.username, email=user.email)
			user_name = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for {}'.format(user_name))
			return redirect('login')
		else:
			print('error while create user: ' + form.errors)
			messages.error(request, 'something went wrong')

	context = {'cartItems': cartItems, 'form': form}

	return render(request, 'user/register.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	print(data)

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):
	data = cartData(request)
	print(data)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)


def order_complete(request):
	data = cartData(request)
	cartItems = data['cartItems']
	context = {'cartItems': cartItems}

	return render(request, 'store/order_complete.html', context)


def is_coupon_valid(request):
	data = json.loads(request.body)
	print(data)
	
	code = data['code']
	
	order = None
	customer = None
	if request.user.is_authenticated:
		customer = Customer.objects.get(user=request.user)
	else:
		customer, _ = Customer.objects.get_or_create(email=data['email'])
		print('not auto customer: ' + str(data['email']))
	
	is_valid = Coupon.is_valid(code, customer)
	if is_valid[0]:
		coupon = Coupon.objects.get(code=code)
		total = None
		if request.user.is_authenticated:
			order_id = data['order_id']
			print('order_id' + order_id)
			order = Order.objects.Order.objects.get_or_create(customer=customer, complete=False)
			order.coupon = coupon
			order.save()
			total = order.get_cart_total
			drop_discount = coupon.get_discount_drop(order.get_original_cart_total)
		else:
			fixed_price = data['total']
			total = coupon.get_discount_price(fixed_price)
			drop_discount = coupon.get_discount_drop(fixed_price)

		return JsonResponse({'is_valid': True, 'coupon': model_to_dict(coupon), 'updated_total': total, 'drop_discount': drop_discount}, safe=False)
	else:
		return JsonResponse({'is_valid':is_valid[0], 'alert':is_valid[1]}, safe=False)

def update_image(request):
	data = json.loads(request.body)
	print(data)

	fb_link = data['fbLink']
	image_id = data['imageId']

	image = Image.objects.get(image_id=image_id)
	image.fb_link = fb_link
	image.remove()
	image.save()

	return JsonResponse('image updated', safe=False)


def updateItem(request):
	data = json.loads(request.body)
	print(data)

	productId = data['productId']
	action = data['action']
	image_id = data['imageId']

	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	print('customer: ' + str(customer))
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(
	    customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(
	    order=order, product=product, image=Image.objects.get(image_id=image_id))

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		if orderItem.quantity == 1:
			messages.success(request, "Item added to cart")
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
		orderItem.image.delete()
		messages.error(request, "Item removed from cart")

	print('Item was added')
	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	print('IN PROCESS ORDER')
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order = Order.objects.get(
		    customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if str(total).strip() == str(order.get_cart_total).strip():
		print('complete order')
		order.complete = True
	print('total from front: "' + str(total).strip() + '" -vs- ' + 'total from back: "' + str(order.get_cart_total).strip() + '"')

	status = data['status']
	if status == 0:
		order.status = 'no_pay'

	order.save()

	ShippingAddress.objects.create(
	customer=customer,
	order=order,
	address=data['shipping']['address'],
	city=data['shipping']['city'],
	zipcode=data['shipping']['zipcode'],
	shipping_type=data['shipping']['shipping_type']
	)
	send_email.send_email('eitan1357@gmail.com', f"מנורת הקסם - קבלה מספר #{order.pk}", 'user/receipt.html', {'order': order})

	return JsonResponse('Payment submitted', safe=False)


class admin_orders(AdminRequiredMixin, ListView):
	model = Order
	context_object_name = 'orders_list'
	template_name = 'admin/admin_orders.html'
	paginate_by = 15
	ordering = ['-date_ordered']

	def get(self, request, *args, **kwargs):
		form = SearchForm(self.request.GET or None)
		if form.is_valid():
			search_query = form.cleaned_data['search_query']
			self.queryset = self.model.objects.filter(pk=search_query, complete=True)
		else:
			self.queryset = self.model.objects.filter(complete=True)


		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = SearchForm(self.request.GET or None)
		context['orders_len'] = len(self.model.objects.all())
		context['orders_closed_len'] = len(self.model.objects.filter(complete=True))
		context['orders_opened_len'] = len(self.model.objects.filter(complete=False))
		return context

class order_details(AdminRequiredMixin, DetailView):
	model = Order
	template_name = 'admin/order_details.html'
	form_class = OrderForm
	paginate_by = 10

	def get_success_url(self):
		return reverse('post_detail', kwargs={'pk': self.object.id})

	def get_context_data(self, **kwargs):
		context = super(order_details, self).get_context_data(**kwargs)
		context['form'] = OrderForm(initial={'status': self.object.status})
		context['admin'] = True
		return context

	def post(self, request, *args, **kwargs):
		form = OrderForm(request.POST)
		if form.is_valid():
			order = self.get_object()
			order.status = form.cleaned_data['status']
			order.save()
			messages.success(request, 'Status saved')
			return redirect('admin_orders')