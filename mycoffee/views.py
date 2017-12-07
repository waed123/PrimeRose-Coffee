from django.shortcuts import render, redirect
from .forms import Signup, Login
from django.contrib.auth import authenticate, login, logout


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
