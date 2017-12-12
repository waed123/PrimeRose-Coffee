from django.urls import path
from . import views


app_name = "mycoffee"

urlpatterns = [
	path('signup/', views.Usersignup ,name="signup"),
	path('login/', views.Userlogin ,name="login"),
	path('logout/', views.Userlogout, name="logout"),
	path('create_coffee/', views.create_coffee, name="create_coffee"),
	path('ajax_price/', views.ajax_price, name="ajax_price"),
	path('coffee_detail/<int:pk>/', views.coffee_detail, name="coffee_detail"),
	path('coffee_list/', views.coffee_list, name="coffee_list"),
]
