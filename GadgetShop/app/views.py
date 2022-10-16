from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

# class based view for showing products on the home page
class ProductView(View):
    def get(self, request):
        laptops = Product.objects.filter(category='L')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'laptops':laptops, 'mobiles':mobiles})

# class based view for showing product details
class ProductDetailView(View):
    def get(self, request, pk):
        products = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'products':products})

# function based view for taking user to the cart page
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

# function based view for showing all products selected by user in cart page
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        shipping_amount = 1000
        total_amount = 0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount})
        else:
            return render(request, 'app/emptycart.html') 

# function based view for increasing quantity of product in cart
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0
        shipping_amount = 1000
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)


# function based view for decreasing quantity of product in cart
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0
        shipping_amount = 1000
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

# function based view for removing product from the cart
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0
        shipping_amount = 1000
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

# function based view buy now page
def buy_now(request):
    return render(request, 'app/buynow.html')

# fucntion based view for address of the customer
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add})

# functin based view for order page
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op})

# function based lview for mobile list
def mobile(request, data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Vivo' or data == 'Samsung' or data == 'Apple' or data =='Asus' or data == 'Realme' or data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

# fuction based view for laptop list
def laptop(request, data=None):
    if data==None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Acer' or data == 'Lenovo' or data == 'Apple' or data =='Asus' or data == 'MSI' or data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptops':laptops})

# class based view for customer registration page 
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congrtulations! Registration Successful')
            form.save()
        return render(request, 'app/customerregistration.html', {'form':form})

# function based view for checkout
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    shipping_amount = 1000
    totalamount = 1000
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:    
        for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

# function based view for paymentdone
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


# class based view for profiles page
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form,})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congrtulations!! Profile Updation Successful")
        return render(request, 'app/profile.html', {'form':form})



