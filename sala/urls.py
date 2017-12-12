from django.urls import path
from . import views


app_name = "sala"

urlpatterns = [
	path('add/', views.add ,name="add"),
]
