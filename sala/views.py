from django.shortcuts import render, redirect
from .models import Cart, CartItem
from mycoffee.models import Coffee
from decimal import Decimal


# Create your views here.
def add(request):
	if request.user.is_anonymous:
		return redirect("mycoffee:login")

	cart, created = Cart.objects.get_or_create(user=request.user)
	item_id = request.GET.get('item_id')
	qty = request.GET.get('qty')

	if item_id:
		coffee = Coffee.objects.get(id=item_id)
		cart_item, created = CartItem.objects.get_or_create(cart=cart, item=coffee)
		if int(qty) < 1:
			cart_item.delete()
		else:
			cart_item.quantity = int(qty)
			cart_item.save()

	return render(request, 'cart.html', {'cart':cart})