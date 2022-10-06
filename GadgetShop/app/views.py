from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

# view for showing products on the home page
class ProductView(View):
    def get(self, request):
        laptops = Product.objects.filter(category='L')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'laptops':laptops, 'mobiles':mobiles})

# view for showing the product details
class ProductDetailView(View):
    def get(self, request, pk):
        products = Product.objects.get(pk=pk)
        return render(request, 'app/productdetail.html', {'products':products})

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return render(request, 'app/addtocart.html')

def buy_now(request):
    return render(request, 'app/buynow.html')

# view for address of the customer
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add})

def orders(request):
    return render(request, 'app/orders.html')

# view for mobile list
def mobile(request, data=None):
    if data==None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Vivo' or data == 'Samsung' or data == 'Apple' or data =='Asus' or data == 'Realme' or data == 'Redmi':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    return render(request, 'app/mobile.html', {'mobiles':mobiles})

# view for laptop list
def laptop(request, data=None):
    if data==None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Acer' or data == 'Lenovo' or data == 'Apple' or data =='Asus' or data == 'MSI' or data == 'HP':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    return render(request, 'app/laptop.html', {'laptops':laptops})

# view for customer registration 
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

def checkout(request):
    return render(request, 'app/checkout.html')

# view for profiles
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