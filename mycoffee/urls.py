from django.urls import path
from . import views


app_name = "mycoffee"

urlpatterns = [
	path('signup/', views.Usersignup ,name="signup"),
	path('login/', views.Userlogin ,name="login"),
	path('logout/', views.Userlogout, name="logout"),
	path('create_coffe/', views.create_coffee, name="create_coffee"),
]
