from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client

from movie_crud.models import MovieContainer

from datetime import datetime
import json

class MoviePostViewsTestCase(TestCase):

	def setUp(self):
		self.c = Client()
		self.createMovie = reverse('createNewMovie')
		self.request_body = {
			"name": "Fractured",
			"description": "this is so good",
			"date_of_release": str(datetime.strptime("2020-12-03", '%Y-%m-%d')).split(" ")[0]
		}

	def test_create_movie(self):
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie -> status_code", response.status_code)
		self.assertEqual(response.status_code, 201)


	def test_create_movie_without_name(self):
		del self.request_body['name']
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie_without_name -> status_code", response.status_code)
		self.assertEqual(response.status_code, 422)

	def test_create_movie_name_is_none(self):
		self.request_body['name'] = None
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie_name_is_none -> status_code", response.status_code)
		self.assertEqual(response.status_code, 422)


	def test_create_movie_without_description(self):
		del self.request_body['description']
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie_without_description -> status_code", response.status_code)
		self.assertEqual(response.status_code, 201)

	def test_create_movie_without_release_date(self):
		del self.request_body['date_of_release']
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie_without_release_date -> status_code", response.status_code)
		self.assertEqual(response.status_code, 422)

	def test_create_movie_release_date_is_empty(self):
		self.request_body['date_of_release'] = ""
		response = self.c.post(self.createMovie, data=json.dumps(self.request_body), content_type='text/json')
		print("test_create_movie_release_date_is_empty -> status_code", response.status_code)
		self.assertEqual(response.status_code, 422)



class MovieGetViewsTestCase(TestCase):

	def setUp(self):
		self.c = Client()

	def test_get_movie_by_id(self):
		movie_obj = MovieContainer.objects.create(name="The Mummy", description="This is a Horror movie", date_of_release=datetime.strptime("2020-12-03", '%Y-%m-%d'))
		self.getMovie = reverse('getMovie', kwargs={'id': movie_obj.id})
		response = self.c.get(self.getMovie)
		print("test_get_movie_by_id -> status_code", response.status_code)
		self.assertEqual(response.status_code, 200)

	def test_get_movie_by_unknown_id(self):
		# movie_obj = MovieContainer.objects.create(name="The Mummy", description="This is a Horror movie", date_of_release=datetime.strptime("2020-12-03", '%Y-%m-%d'))
		self.getMovie = reverse('getMovie', kwargs={'id': 12})
		response = self.c.get(self.getMovie)
		print("test_get_movie_by_unknown_id -> status_code: ", response.status_code)
		self.assertEqual(response.status_code, 404)
		
class MovieUpdateViewsTestCase(TestCase):

	def setUp(self):
		self.c = Client()
		self.movie_obj = MovieContainer.objects.create(name="The Mummy", description="This is a Horror movie", date_of_release=datetime.strptime("2020-12-03", '%Y-%m-%d'))
		self.updateMovie = reverse('updateMovie', kwargs={'id': self.movie_obj.id})


	def test_update_movie_name_by_id(self):
		request_body = {
			"name": "The Mummy part 2"
		}
		response = self.c.put(self.updateMovie, data=json.dumps(request_body), content_type='text/json')
		self.assertEqual(response.status_code, 200)
		print("test_update_movie_name_by_id -> status_code", response.status_code)

		# checkout the updated data
		movie_obj_2 = MovieContainer.objects.get(id=self.movie_obj.id)
		self.assertEqual(movie_obj_2.name, request_body['name'])

	def test_update_movie_description_by_id(self):
		request_body = {
			"description": "This is a Horror movie with more advature"
		}
		response = self.c.put(self.updateMovie, data=json.dumps(request_body), content_type='text/json')
		self.assertEqual(response.status_code, 200)
		print("test_update_movie_description_by_id -> status_code", response.status_code)

		# checkout the updated data
		movie_obj_2 = MovieContainer.objects.get(id=self.movie_obj.id)
		self.assertEqual(movie_obj_2.description, request_body['description'])

	def test_update_movie_detail_by_id(self):
		request_body = {
			"name": "The Mummy 2",
			"description": "This is a Horror movie with more advature",
			"date_of_release": str(datetime.strptime("2021-01-03", '%Y-%m-%d')).split(" ")[0]
		}		
		response = self.c.put(self.updateMovie, data=json.dumps(request_body), content_type='text/json')
		self.assertEqual(response.status_code, 200)
		# checkout the updated data
		movie_obj_2 = MovieContainer.objects.get(id=self.movie_obj.id)
		print("test_update_movie_detail_by_id -> status_code", response.status_code)

		self.assertEqual(movie_obj_2.name, request_body['name'])
		self.assertEqual(movie_obj_2.description, request_body['description'])
		self.assertEqual(str(movie_obj_2.date_of_release), request_body['date_of_release'])

	def test_update_movie_by_id(self):
		request_body = {}
		response = self.c.put(self.updateMovie, data=json.dumps(request_body), content_type='text/json')
		self.assertEqual(response.status_code, 200)
		print("test_update_movie_by_id -> status_code", response.status_code)

		# checkout the updated data
		movie_obj_2 = MovieContainer.objects.get(id=self.movie_obj.id)
		self.assertEqual(self.movie_obj, movie_obj_2)


class MovieDViewsTestCase(TestCase):
	def setUp(self):
		self.c = Client()
		self.movie_obj = MovieContainer.objects.create(name="The Mummy", description="This is a Horror movie", date_of_release=datetime.strptime("2020-12-03", '%Y-%m-%d'))
		self.deleteMovie = reverse('deleteMovie', kwargs={'id': self.movie_obj.id})

	def test_delete_movie_by_id(self):
		response = self.c.delete(self.deleteMovie)
		print("test_delete_movie_by_id -> status_code", response.status_code)
		self.assertEqual(response.status_code, 204)
		movie_obj_2 = None
		try:
			movie_obj_2 = MovieContainer.objects.get(id=self.movie_obj.id) 
		except ObjectDoesNotExist:
			pass
		self.assertEqual(movie_obj_2, None)

	def test_delete_movie_by_unknown_id(self):
		self.deleteMovie = reverse('deleteMovie', kwargs={'id': 12})
		response = self.c.delete(self.deleteMovie)
		print("test_delete_movie_by_unknown_id -> status_code", response.status_code)
		self.assertEqual(response.status_code, 404)
