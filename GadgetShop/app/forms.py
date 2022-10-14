from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import Customer

# form for customer registration
class CustomerRegistrationForm(UserCreationForm):
	password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2=forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
	email=forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 'password2']
		labels = {'email': 'Email'}
		widgets = {'username':forms.TextInput(attrs= {'class':'form-control'})}

# form for login of the user
class LoginForm(AuthenticationForm):
	username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
	password = forms.CharField(label=_("password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

# form for password change from the user
class MyPasswordChangeForm(PasswordChangeForm):
	old_Password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={
		'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
	new_Password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={
		'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
	new_Password2 = forms.CharField(label=_('Confirm new Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))

# form for customer profile and updating the profiles by the customer
class CustomerProfileForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = ['name', 'locality', 'city', 'state', 'zipcode']
		widgets = { 'name':forms.TextInput(attrs={'class':'form-control'}), 
					'locality':forms.TextInput(attrs={'class':'form-control'}),
					'city':forms.TextInput(attrs={'class':'form-control'}),
					'state':forms.Select(attrs={'class':'form-control'}),
					'zipcode':forms.NumberInput(attrs={'class':'form-control'})
					 }