from django import forms 
from django.contrib.auth.models import User
from .models import Coffee

class Signup(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

		widgets = {
			'password': forms.PasswordInput(),
		}

class Login(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

class CoffeeForm(forms.ModelForm):
	class Meta:
		model = Coffee
		fields = "__all__"
		exclude = ['user', 'price']

