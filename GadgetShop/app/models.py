from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# variable which contains the list of states
STATE_CHOICES = (
	('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
	('Andhra Pradesh','Andhra Pradesh'),
	('Arunachal Pradesh','Arunachal Pradesh'),
	('Assam','Assam'),
	('Bihar','Bihar'),
	('Chandigarh','Chandigarh'),
	('Chattisgarh','Chattisgarh'),
	('Goa','Goa'),
	('Gujarat','Gujarat'),
	('Haryana','Haryana'),
	('Kerala','Kerala'),
	('Manipur','Manipur'),
	('Nagaland','Nagaland'),
	('Meghalya','Meghalya'),
	('Jharkhand','Jharkhand'),
	('Madhya Pradesh','Madhya Pradesh'),
	('Rajasthan','Rahjasthan'),
	('Uttar Pradesh','Uttar Pradesh'),
	('Tamil Nadu','Tamil Nadu'),
	)

# models for new customer
class Customer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	locality = models.CharField(max_length=200)
	city = models.CharField(max_length=50)
	zipcode = models.IntegerField()
	state = models.CharField(choices=STATE_CHOICES, max_length=50)

	def __str__(self):
		return str(self.id)

# variable which contains the list of product choices
CATEGORY_CHOICES = (
	('M','Mobile'),
	('L','laptop'),
	)
	
# model which contains the list of product 
class Product(models.Model):
	title = models.CharField(max_length=100)
	selling_price = models.FloatField()
	discounted_price = models.FloatField()
	description = models.TextField()
	brand = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
	product_image = models.ImageField(upload_to='producting')

	def __str__(self):
		return str(self.id)

# model which contains the product chosed by the user
class Cart(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	@property
	def total_cost(self):
		return self.quantity * self.product.selling_price
	

# vaible showing the status of the product
STATUS_CHOICES = (
	('Accepted','Accepted'),
	('Packed','Packed'),
	('On The Way','On The Way'),
	('Delivered','Delivered'),
	('Cancel','Cancel')
	)

# model showing the list of order placed 
class OrderPlaced(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)
	ordered_date = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')