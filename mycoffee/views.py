from django.shortcuts import render, redirect
from .forms import Signup, Login, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal


def Usersignup(request):
	context = {}
	form = Signup()
	context['form'] = form
	if request.method == 'POST':
		form = Signup(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("mycoffee:coffeelist")
		return redirect("mycoffee:signup")
	return render(request, 'signup.html', context)

def Userlogin(request):
	context = {}
	form = Login()
	context['form'] = form
	if request.method == 'POST':
		form = Login(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("mycoffee:coffeelist")
		return redirect("mycoffee:login")
	return render(request, 'login.html', context)


def Userlogout(request):
	logout(request)
	return redirect("mycoffee:coffeelist")


def coffee_price(instance):
	total = instance.bean.price + instance.roast.price + (instance.espresso_shots*Decimal(0.250))
	if instance.steamed_milk:
		total += Decimal(0.100)
	if instance.powders.all().count()>0:
		for powder in instance.powders.all():
			total += powder.price
	if instance.syrups.all().count()>0:
		for syrup in instance.syrups.all():
			total+= syrup.price
	return total


def create_coffee(request):
	context = {}
	if not request.user.is_authenticated:
		return redirect("mycoffee:login")
		
	form = CoffeeForm()
	if request.method == "POST":
		form = CoffeeForm(request.POST)
		if request.is_valid():
			coffee = form.save(commit=False)
			coffee.user = request.user
			coffee.save()
			form.save_m2m() #this is requiered when I assign orm.save(commit=False) and there is ManyToMany relations 
			coffe.price = coffee_price(coffee)
			coffee.save()
			return redirect("mycoffee:coffeelist")
	context['form'] = form
	return render(request, 'create_coffee.html', context)

