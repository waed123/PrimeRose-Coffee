from django.db import models
from django.contrib.auth.models import User

class Bean(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=3)

	def __str__(self):
		return self.name

class Roast(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=3)

	def __str__(self):
		return self.name

class Syrup(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=3)

	def __str__(self):
		return self.name

class Powder(models.Model):
	name = models.CharField(max_length=200)
	price = models.DecimalField(max_digits=5, decimal_places=3)

	def __str__(self):
		return self.name


class Coffee(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	name = models.CharField(max_length=200)
	espresso_shots = models.PositiveIntegerField(default=1)
	bean = models.ForeignKey(Bean, on_delete=models.PROTECT)
	roast = models.ForeignKey(Roast, on_delete=models.PROTECT)
	syrups = models.ManyToManyField(Syrup, blank=True)
	powders = models.ManyToManyField(Powder, blank=True)
	water = models.FloatField()
	steamed_milk = models.BooleanField(default=False)
	foam = models.FloatField()
	extra_instructions = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=5, decimal_places=3, null=True)

	def __str__(self):
		return self.name
