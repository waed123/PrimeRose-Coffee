from django.shortcuts import render, redirect
from .forms import Signup, Login, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.http import JsonResponse, Http404
from .models import Bean, Roast, Syrup, Powder, Coffee
import json


def coffee_list(request):
	if request.user.is_anonymous:
		return redirect("mycoffee:login")

	coffee_list = Coffee.objects.filter(user=request.user)
	context = {
		'coffee_list': coffee_list,
	}
	return render(request, 'coffee_list.html', context)


def coffee_detail(request, pk):
	if request.user.is_anonymous:
		return redirect("mycoffee:login")

	coffee = Coffee.objects.get(pk=pk)
	if not (request.user == coffee.user or request.user.is_superuser or request.user.is_staff):
		raise Http404
	context = {
		'coffee': coffee,
	}

	return render(request, 'coffee_detail.html', context)

def ajax_price(request):
	total_price = Decimal(0)

	bean_id = request.GET.get('bean')
	if bean_id:
		total_price += Bean.objects.get(id=bean_id).price

	roast_id = request.GET.get('roast')
	if roast_id:
		total_price += Roast.objects.get(id=roast_id).price

	syrups = json.loads(request.GET.get('syrups'))
	if len(syrups) >0:
		for syrup_id in syrups:
			total_price += Syrup.objects.get(id=syrup_id).price

	powders = json.loads(request.GET.get('powders'))
	if len(powders)>0:
		for powder_id in powders:
			total_price += Powder.objects.get(id=powder_id).price

	milk = request.GET.get('milk')
	if milk=='true':
		total_price += Decimal(0.100)

	shots=request.GET.get('espresso_shots')
	if shots:
		total_price += Decimal(int(shots)*(0.250))

	return JsonResponse(round(total_price,3), safe=False)



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

			return redirect("mycoffee:coffee_list")
		return redirect("mycoffee:signup")
	return render(request, 'signup.html', context)

def Userlogin(request):
	context = {}
	form = Login()
	context['form'] = form
	if request.method == "POST":
		form = Login(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("mycoffee:coffee_list")
		return redirect("mycoffee:login")
	return render(request, 'login.html', context)


def Userlogout(request):
	logout(request)
	return redirect("mycoffee:coffee_list")


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
		if form.is_valid():
			coffee = form.save(commit=False)
			coffee.user = request.user
			coffee.save()
			form.save_m2m() #this is requiered when I assign orm.save(commit=False) and there is ManyToMany relations 
			coffee.price = coffee_price(coffee)
			coffee.save()
			return redirect("mycoffee:coffee_list")
	context['form'] = form
	return render(request, 'create_coffee.html', context)

