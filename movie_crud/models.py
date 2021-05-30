from django.db import models

# Create your models here.


class MovieContainer(models.Model):
	id = models.AutoField(primary_key=True, auto_created=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=500, null=True)
	date_of_release = models.DateField(auto_now=False, auto_now_add=False)

	def toJson(self):
		return {
			"id": self.id,
			"name": self.name,
			"description": self.description,
			"date_of_release": str(self.date_of_release)
		}
