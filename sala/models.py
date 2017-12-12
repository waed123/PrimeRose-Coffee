from django.db import models
from mycoffee.models import Coffee
from django.contrib.auth.models import User
from decimal import Decimal
from django.db.models.signals import pre_save, post_save, post_delete 
#pre_save used to save some data that it shouls generated automatically in models

class CartItem(models.Model):
	cart = models.ForeignKey("Cart", on_delete=models.PROTECT) #Cart is in quotes, we did that because we are using the model before defining it.
	item = models.ForeignKey(Coffee, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField(default=1) #Define how many of this item do I want.
	line_item_total = models.DecimalField(decimal_places = 3, max_digits = 20) #total price of the specific item (item price x quantity)

	#define default value for the object
	def __str__(self):
		return str(self.item.name)


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	if qty>=1:
		price = instance.item.price
		line_item_total = price * qty
		instance.line_item_total = line_item_total
		#instance.save() its cause infinte loop since system after call pre_save its automatically saved so when but save inside pre_save its save and call pre_save again

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


#After save and delete the cartitem object; call  cart_item_post_save_receiver to update subtotal for the cart
def cart_item_post_save_receiver(instance, *args, **kwargs):
	instance.cart.calc_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)
post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
	items = models.ManyToManyField(Coffee, through=CartItem)
	subtotal = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
	delivery_total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
	total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)

	def __str__(self):
		return str(self.id)

	#calc_subtotal is Model method
	def calc_subtotal(self):
		sub = Decimal(0)
		items = self.cartitem_set.all() #retrieve all cart items that related to the card
		for item in items:
			sub += item.line_item_total
		self.subtotal = sub #round of 3 decimial places
		#sub += self.delivery_total
		#self.total = "%.3f"%sub #round of 3 decimial places
		self.save()

def do_delivery_and_total(instance, *args, **kwargs):
	instance.total = instance.subtotal + instance.delivery_total

pre_save.connect(do_delivery_and_total, sender=Cart)