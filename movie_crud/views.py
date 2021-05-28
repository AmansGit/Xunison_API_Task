from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import MovieContainer
# Create your views here.

import json
from datetime import datetime

@csrf_exempt
def createNewMovie(request):
	response = {}
	if request.method=='POST':
		movies = json.loads(request.body)
		name = movies['name']
		description = movies['description']
		dor = datetime.strptime(movies['date_of_release'], '%Y-%m-%d')

		# name = request.body['name']
		# description = request.body['description']
		# date_of_release = request.body['date_of_release']

		print("date_of_release:: ", dor)
		print("name:: ", name)

		c_movie = MovieContainer(name=name, description=description, date_of_release=dor)
		try:
			print(c_movie)
			c_movie.save()			
			movie_obj = MovieContainer.objects.filter(name=name).first()
			# response.success('message', data. 200)
			response = {
				"msg": "Created successfully",
				"status": 200,
				"data":{
						"id": movie_obj.id,
						"name": movie_obj.name,	
					}				
			}

		except:
			response = {
				"msg": "Something went wrong",
				"status": 400,
				"data": None
			}

	return HttpResponse(json.dumps(response), content_type='text/json')


def getMovie(request, id=None):
	response = {}
	data = []
	
	if request.method == 'GET':
		try:
			if id == None:

				print
				movie_obj = MovieContainer.objects.all()
				for obj in movie_obj:
					d = {
						"id": obj.id,
						"name": obj.name
					}
					data.append(d)
				msg = "All data is extracted"
			else:
				movie_obj = MovieContainer.objects.filter(id=id).first()
				print("OBJ:: ", movie_obj)
				data = {
					"id": movie_obj.id,
					"name": movie_obj.name
				}
				msg = "One data is extracted"
		except:
			msg = "Something went wrong."
			data = None

	response = {
		"msg": msg,
		"data": data
	}

	return HttpResponse(json.dumps(response), content_type='text/json')



def updateMovie(request, id):
	response = {}
	
	if request.method=='PUT':

		movies = json.loads(request.body)
		id = movies['id']
		name = movies['name']
		description = movies['description']
		dor = movies['date_of_release']
		try:
			movie_obj = MovieContainer.objects.filter(id=id).first()
			movie_obj.name = name
			movie_obj.description = description
			movie_obj.date_of_release = dor

			# MovieContainer(name=name, description=description, date_of_release=dor)

			response = {
				"msg": "Successfully updated",
				"data":{
					"id": movie_obj.id,
					"name": movie_obj.name
				}
			}
		except:
			response = {
				"msg": "Not updated",
				"data": None
			}

	return HttpResponse(json.dumps(response), content_type='text/json')


def deleteMovie(request, id):
	response = {}
	if request.method == 'DELETE':
		movies = json.loads(request.body)

		id = movies['id']
		movie_obj = MovieContainer.objects.get(id=id)

		try:
			response = {
				"msg": "Successfully delete",
				"data": {
					"id": movie_obj.id,
					"name": "movie_obj.name"
				}
			}
			movie_obj.delete()

		except:
			response = {
				"msg": "Something went wrong, id not found",
				"data": None
			}

	return HttpResponse(json.dumps(response), content_type='text/json')
