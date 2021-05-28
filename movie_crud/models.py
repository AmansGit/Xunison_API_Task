from django.db import models

# Create your models here.


class MovieContainer(models.Model):
	id = models.AutoField(primary_key=True, auto_created=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500)
	date_of_release = models.DateField(auto_now=False, auto_now_add=False)
