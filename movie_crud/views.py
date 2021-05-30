import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from .models import MovieContainer
from .validations import movie_request_validation

@csrf_exempt
def createNewMovie(request):
	response = {}
	if request.method=='POST':
		v_status = True
		v_msg = ""
		v_status, v_msg = movie_request_validation(json.loads(request.body))

		if v_status:
			movies = json.loads(request.body)
			name = movies['name']
			description = ('description' in movies and movies['description']) or None
			dor = datetime.strptime(movies['date_of_release'], '%Y-%m-%d')

		# ---------- filter-out duplicate data on the basis of movie name ---------------
			c_movie = MovieContainer.objects.filter(name=name).first()
			if c_movie is not None:
				id = c_movie.id
				response = {
					"msg": "Data is already present in DB, please use UPDATE to change data",
					"data": c_movie.toJson()
				}
				status = 409

			else:
				c_movie = MovieContainer(name=name, description=description, date_of_release=dor)
				try:
					c_movie.save()
					movie_obj = MovieContainer.objects.get(id=c_movie.id)
					response = {
						"msg": "Created successfully",
						"data": movie_obj.toJson()
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
					d = obj.toJson()
					data.append(d)
				msg = "All data is extracted"
				status = 200
			else:
				movie_obj = MovieContainer.objects.get(id=id)
				data = movie_obj.toJson()
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
		name = 'name' in movies and movies['name'] or None
		description = 'description' in movies and movies['description'] or None
		dor = 'date_of_release' in movies and movies['date_of_release'] or None
		try:
			movie_obj = MovieContainer.objects.get(id=id)
			if(not name and not description and not dor):
				response = {
					"msg": "No value to update",
					"data": movie_obj.toJson()
				}
			else:
				if(name):
					movie_obj.name = name
				if(description):
					movie_obj.description = description
				if(dor):
					movie_obj.date_of_release = dor
				movie_obj.save()

				response = {
					"msg": "Successfully updated",
					"data": movie_obj.toJson()
				}
			status = 200

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
				"data": movie_obj.toJson()
			}
			movie_obj.delete()
			status = 204

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
	return HttpResponse(json.dumps(response), content_type='text/json', status=status)
