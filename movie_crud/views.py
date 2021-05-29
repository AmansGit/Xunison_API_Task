import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import MovieContainer
from .validations import key_validation

@csrf_exempt
def createNewMovie(request):
	response = {}
	if request.method=='POST':
		v_status = True
		v_msg = ""
		v_status, v_msg = key_validation(json.loads(request.body))

		if v_status:
			movies = json.loads(request.body)
			name = movies['name']
			description = movies['description']
			dor = datetime.strptime(movies['date_of_release'], '%Y-%m-%d')

		# ---------- filter-out duplicate data on the basis of movie name ---------------
			c_movie = MovieContainer.objects.filter(name=name).first()
			if c_movie is not None:
				id = c_movie.id
				response = {
					"msg": "Data is already present in DB, please use UPDATE to change data",
					"data":{
						"id": c_movie.id,
						"name": c_movie.name,
						"description": c_movie.description,
						"date of release": str(c_movie.date_of_release)
					}
				}
				status = 409

			else:
				c_movie = MovieContainer(name=name, description=description, date_of_release=dor)
				try:
					c_movie.save()
					movie_obj = MovieContainer.objects.get(id=c_movie.id)
					# response.success('message', data. 200)
					response = {
						"msg": "Created successfully",
						"data":{
								"id": movie_obj.id,
								"name": movie_obj.name,
								"description": movie_obj.description,
								"date of release": str(movie_obj.date_of_release)
							}				
					}
					status = 201

				except:
					response = {
						"msg": "Something went wrong",
						"data": None
					}
					status = 400
		else:
			response = {
				"msg": v_msg,
				"data": None
			}
			status = 422

	return HttpResponse(json.dumps(response), content_type='text/json', status=status)


def getMovie(request, id=None):
	response = {}
	data = []
	
	if request.method == 'GET':
		try:
			if id == None:
				movie_obj = MovieContainer.objects.all()
				for obj in movie_obj:
					d = {
						"id": obj.id,
						"name": obj.name
					}
					data.append(d)
					print("DATE:: ", obj.date_of_release)
				msg = "All data is extracted"
				status = 200
			else:
				movie_obj = MovieContainer.objects.get(id=id)
				print("OBJ:: ", movie_obj)
				data = {
					"id": movie_obj.id,
					"name": movie_obj.name
				}
				msg = "One data is extracted"
				status = 200

		except ObjectDoesNotExist:
			msg = f"Data is not present with id: {id}"
			data = None
			status = 404
		except Exception as e:
			msg = "Something went wrong."
			data = None
			status = 500

	response = {
		"msg": msg,
		"data": data
	}

	return HttpResponse(json.dumps(response), content_type='text/json', status=status)


@csrf_exempt
def updateMovie(request, id):
	response = {}
	
	if request.method=='PUT':

		movies = json.loads(request.body)
		# id = movies['id']
		name = movies['name']
		description = movies['description']
		dor = movies['date_of_release']
		try:
			movie_obj = MovieContainer.objects.get(id=id)
			movie_obj.name = name
			movie_obj.description = description
			movie_obj.date_of_release = dor
			movie_obj.save()

			# MovieContainer(name=name, description=description, date_of_release=dor)

			response = {
				"msg": "Successfully updated",
				"data":{
					"id": movie_obj.id,
					"name": movie_obj.name
				}
			}
			status = 201

		except ObjectDoesNotExist:
			response = {
				"msg": f"Data is not present with id: {id}",
				"data": None
			}
			status = 404
		except Exception as e:
			response = {
				"msg": "Not updated",
				"data": None
			}
			status = 500

	return HttpResponse(json.dumps(response), content_type='text/json', status=status)


@csrf_exempt
def deleteMovie(request, id=id):
	response = {}
	if request.method == 'DELETE':
		try:
			movie_obj = MovieContainer.objects.get(id=id)
			response = {
				"msg": "Successfully delete",
				"data": {
					"id": movie_obj.id,
					"name": movie_obj.name
				}
			}
			movie_obj.delete()
			status = 410

		except ObjectDoesNotExist:
			response = {
				"msg": f"Data is not present with id: {id}",
				"data": None
			}
			status = 404

		except:
			response = {
				"msg": "Something went wrong, id not found",
				"data": None
			}
			status = 400

	return HttpResponse(json.dumps(response), content_type='text/json')
